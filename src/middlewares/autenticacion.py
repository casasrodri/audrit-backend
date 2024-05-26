from fastapi import FastAPI, Request, Depends, status
from typing import Annotated
from entidades.usuarios.model import UsuarioAutenticacion
from utils.jwt import leer_token
from jose.exceptions import JWTError
from fastapi import status
from fastapi.responses import JSONResponse
from mocks.database import DatabaseMock
from fastapi import APIRouter, HTTPException
from utils.logger import logger


# Dependencia para obtener los datos del usuario a partir de la cookie
async def __obtener_usuario_logueado(request: Request) -> UsuarioAutenticacion:
    usuario: UsuarioAutenticacion = request.state.user
    return usuario


EsteUsuario = Annotated[UsuarioAutenticacion, Depends(__obtener_usuario_logueado)]

PATH_PUBLICOS = [
    "/docs",
    "/openapi.json",
    "/api/v1/jwt",
    "/api/v1/jwt_debug",
    "/api/v1/logout",
]
PATH_PUBLICOS.extend(
    [
        "/api/v1/users",
        "/api/v1/users",
        "/mascotas",
        "/api/v1/ciclos/",
        "/api/v1/ciclos/nodos",
        "/api/v1/",
    ]
)
# PATH_PUBLICOS.append("/")


def autenticacion_midd(app: FastAPI):
    # print("Inicializando middleware de autenticación...")

    # TODO: Hacerlo como una funcion, que luego es importada por la app... tipo app.add_middleware(mi_funcion)
    # TODO: ver si primero verifica vista publica, caso que no sea publica, obtiene el usuario y lo agrega al request.state, y luego llama al de autorización.
    @app.middleware("http")
    async def autenticacion(request: Request, call_next):
        path = request.scope.get("path")
        query = request.scope.get("query_string").decode()
        jwt = request.cookies.get("jwt")

        logger.who(f"{path=}, {query=}, {jwt=}")

        if path in PATH_PUBLICOS:
            logger.who("No se requiere autenticación!")
            response = await call_next(request)
            return response

        logger.who("Autenticando al usuario...")

        email_jwt = None
        try:
            email_jwt = await leer_token(jwt)
            logger.who(email_jwt)

        except JWTError as jwt_e:
            # logger.who(f"JWTError: {jwt_e}")
            logger.who("No se pudo validar el token de acceso.")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "No se pudo validar el token de acceso."},
                # headers={"WWW-Authenticate": "Bearer"},
            )

        except AttributeError as attr_e:
            # logger.who(f"AttributeError: {attr_e}")
            logger.who("No se encontró el token de acceso.")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "No se encontró el token de acceso."},
                # headers={"WWW-Authenticate": "Bearer"},
            )

        except Exception as e:
            logger.who("{type(e)}: {e}")
            logger.who("Error desconocido al procesar el JWT.")

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error desconocido al procesar el JWT."},
            )

        # Agrega el valor de la cookie al contexto del request
        db = DatabaseMock()
        usuario: UsuarioAutenticacion = db.obtener_usuario_por_email(email_jwt)

        request.state.user = usuario
        print(f"Usuario autenticado: {usuario}")

        # Llama a la siguiente función en la cadena de middleware
        response = await call_next(request)
        return response
