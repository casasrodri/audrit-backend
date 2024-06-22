from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from jose.exceptions import JWTError
from utils.jwt import leer_token
from utils.logger import logger
from database import get_db
from entidades.usuarios.controller import UsuariosController
from middlewares.auth.schema import EndpointDB
from entidades.usuarios.schema import UsuarioDB

PATH_PUBLICOS = [
    "/docs",
    "/openapi.json",
    "/api/v1/sesiones/jwt",
    "/",
]


# AUTENTICACIÓN
class TokenException(HTTPException):
    def __init__(self, mensaje: str, status: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(
            status_code=status,
            detail=mensaje,
        )
        logger.who(f"TokenException: {mensaje}")


async def obtener_email(jwt: str) -> str:
    try:
        return await leer_token(jwt)

    except JWTError:
        # logger.who(f"JWTError: {jwt_e}")
        raise TokenException(
            mensaje="No se pudo validar el token de acceso.",
        )

    except AttributeError:
        # logger.who(f"AttributeError: {attr_e}")
        raise TokenException(
            mensaje="No se encontró el token de acceso.",
        )

    except Exception:
        # logger.who("{type(e)}: {e}")

        raise TokenException(
            mensaje="Error desconocido al procesar el JWT.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# AUTORIZACIÓN
def get_endpoint_response(request: Request) -> tuple:
    for route in request.app.router.routes:
        if isinstance(route, APIRoute):
            _, sco = route.matches(request)
            if sco:
                route = sco["route"]
                return route.path, route.methods


# MIDDELWARE
async def auth_middleware(request: Request, call_next):
    # Variables de contexto
    method = request.scope.get("method")
    path = request.scope.get("path")
    # query = request.scope.get("query_string").decode()
    jwt = request.cookies.get("jwt")
    # user: UsuarioDB = request.scope.get("state").get("user")
    db = next(get_db())

    if path in PATH_PUBLICOS:
        logger.who("Endpoint público")
        return await call_next(request)

    # AUTENTICACIÓN
    # Se obtiene el email del token
    try:
        email_jwt = await obtener_email(jwt)
        # logger.who(email_jwt)
    except TokenException as token_e:
        return JSONResponse(
            status_code=token_e.status_code,
            content={"error": token_e.detail},
        )

    # Se busca el usuario y se agrega al contexto
    user: UsuarioDB = await UsuariosController.get_by_email(db, email_jwt)
    request.state.user = user
    logger.who(f"{user.nombre} {user.apellido}")

    # AUTORIZACION
    # Se determina el endpoint de respuesta
    try:
        endpoint_path, endpoint_methods = get_endpoint_response(request)
    except TypeError:
        return JSONResponse(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            content={"message": "Endpoint no implementado"},
        )
    endpoint_requested = EndpointDB(method=method, path=endpoint_path)

    if endpoint_requested not in user.rol.endpoints:
        logger.can(
            f"El usuario {user.nombre} {user.apellido} [{user.rol.nombre}] no tiene permisos para acceder "
            f"a [{method}] {endpoint_path}"
        )
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "No autorizado"},
        )

    logger.can("Acceso permitido.")
    db.close()
    # Se continua con las demás llamadas
    response = await call_next(request)
    return response
