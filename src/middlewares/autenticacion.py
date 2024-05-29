from fastapi import Request, status, HTTPException
from utils.jwt import leer_token
from jose.exceptions import JWTError
from fastapi import status
from fastapi.responses import JSONResponse
from utils.logger import logger
from database import get_db
from entidades.usuarios.controller import UsuariosController


class TokenException(HTTPException):
    def __init__(self, mensaje: str, status: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(
            status_code=status,
            detail=mensaje,
        )


PATH_PUBLICOS = [
    "/docs",
    "/openapi.json",
    "/api/v1/sesiones/jwt",
    # "/",
]


async def obtener_email(jwt: str) -> str:
    try:
        return await leer_token(jwt)

    except JWTError as jwt_e:
        logger.who(f"JWTError: {jwt_e}")
        logger.who("No se pudo validar el token de acceso.")
        raise TokenException(
            mensaje="No se pudo validar el token de acceso.",
        )

    except AttributeError as attr_e:
        logger.who(f"AttributeError: {attr_e}")
        logger.who("No se encontró el token de acceso.")
        raise TokenException(
            mensaje="No se encontró el token de acceso.",
        )

    except Exception as e:
        logger.who("{type(e)}: {e}")
        logger.who("Error desconocido al procesar el JWT.")

        raise TokenException(
            mensaje="Error desconocido al procesar el JWT.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# def autenticacion_midd(app: FastAPI):
#     @app.middleware("http")
async def autenticacion(request: Request, call_next):
    # Variables de contexto
    path = request.scope.get("path")
    # query = request.scope.get("query_string").decode()
    jwt = request.cookies.get("jwt")

    # logger.who(f"{path=}, {query=}, {jwt=}")

    if path in PATH_PUBLICOS:
        logger.who("Endpoint público")
        return await call_next(request)

    # Se obtiene el email del token
    try:
        email_jwt = await obtener_email(jwt)
        # logger.who(email_jwt)
    except TokenException as token_e:
        return JSONResponse(
            status_code=token_e.status_code,
            content={"error": token_e.detail},
        )

    # Se busca el usuario
    db = next(get_db())
    usuario = await UsuariosController.get_by_email(db, email_jwt)

    # Agrega el valor de la cookie al contexto del request
    request.state.user = usuario
    logger.who(f"{usuario.nombre} {usuario.apellido}")

    # Llama a la siguiente función en la cadena de middleware
    response = await call_next(request)
    return response
