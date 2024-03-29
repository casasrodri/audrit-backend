from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from models.usuarios import UsuarioLogin
from middlewares.autenticacion import EsteUsuario
from models.usuarios import UsuarioOut
from utils.jwt import crear_token, JWT_EXPIRE_MINUTES
from utils.logger import logger
from controllers.usuarios import validar_credenciales

router = APIRouter()


class CredencialesException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
            headers={"WWW-Authenticate": "Bearer"},
        )


COOKIES_KWARGS = {
    "httponly": True,
    "secure": True,
    "samesite": "None",
    "expires": JWT_EXPIRE_MINUTES * 60,
}


@router.post("/jwt")
async def login(credenciales: UsuarioLogin, response: Response):
    # 1. Verifico que los datos sean correctos
    try:
        await validar_credenciales(credenciales.email, credenciales.password)
    except Exception as e:
        logger.error(f"Error al validar credenciales: {e}")
        raise CredencialesException()

    # 2. Genero el token de acceso
    token_data = {"sub": credenciales.email}
    access_token = await crear_token(token_data)

    # 3. Guardo el token de acceso en una cookie
    response.set_cookie(key="jwt", value=access_token, **COOKIES_KWARGS)
    # response.set_cookie(key="nombre", value="Rodriii 2.1", **COOKIES_KWARGS)
    response.set_cookie(
        key="nombre",
        value="Rodri",
        secure=True,
        httponly=False,
        samesite="None",
        expires=JWT_EXPIRE_MINUTES * 60,
    )
    # TODO Agregar acá demás datos que le sirvan al front, como los menús que podrá ver

    # 4. Devuelvo el resultado del login
    return {
        "status": "ok",
        "description": "Login correcto.",
        "jwt": access_token,
    }


# http://localhost:8000/jwt_debug?email=rodri&password=rodri
@router.get("/jwt_debug")
async def login_con_query_params(email: str, password: str, response: Response):
    logger.trace(f"Parámetros de jwt_debug: {email=} {password=}")

    if email == "rodri":
        email = "rodri@casas.com"

    if password == "rodri":
        password = "rodri"

    usuario = UsuarioLogin(email=email, password=password)
    logger.info(repr(usuario))

    return await login(usuario, response)


# Path operation que utiliza la dependencia para obtener los datos del usuario
@router.get("/usuario", response_model=UsuarioOut)
async def obtener_datos_usuario_logueado(usuario: EsteUsuario):
    return usuario


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="jwt")
    return {"status": "ok", "message": "Logout correcto."}


@router.get("/menues")
async def obtener_menues(usuario: EsteUsuario):
    return {
        "usuario": usuario,
        "menues": [
            {"nombre": "Auditorías", "url": "/auditorias"},
            {"nombre": "Observaciones", "url": "/observaciones"},
            {"nombre": "Requerimientos", "url": "/requerimientos"},
        ],
    }
