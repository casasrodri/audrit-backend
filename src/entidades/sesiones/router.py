from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.responses import Response
from utils.jwt import crear_token, JWT_EXPIRE_MINUTES
from utils.logger import logger
from entidades.usuarios.controller import UsuariosController
from entidades.usuarios.model import UsuarioLogin, UsuarioOut
from database import SqlDB
from entidades.usuarios.controller import CredencialesException
from typing import Annotated
from entidades.usuarios.schema import UsuarioDB


# Depende de que el middleware de autenticación haya sido ejecutado
async def __obtener_usuario_logueado(request: Request) -> UsuarioOut:
    usuario: UsuarioDB = request.state.user
    return usuario


EsteUsuario = Annotated[UsuarioOut, Depends(__obtener_usuario_logueado)]


router = APIRouter()


COOKIES_KWARGS = {
    "httponly": True,
    # "secure": True,       # Solo para HTTPS
    # "samesite": "None",   # Solo para HTTPS
    "expires": JWT_EXPIRE_MINUTES * 60,
}


@router.post("/jwt")
async def login(db: SqlDB, credenciales: UsuarioLogin, response: Response):
    # 1. Busco el usuario a loguear
    try:
        user = await UsuariosController.get_by_email(db, credenciales.email)
    except HTTPException:
        raise CredencialesException()

    # 2. Verifico que las credenciales
    await UsuariosController.validar_credenciales(user, credenciales.password)

    # 3. Genero el token de acceso
    token_data = {"sub": credenciales.email}
    access_token = await crear_token(token_data)

    # 4. Guardo el token de acceso en una cookie
    response.set_cookie(key="jwt", value=access_token, **COOKIES_KWARGS)
    logger.who("Se envía cookie con token de acceso.")

    # 4. Devuelvo el resultado del login
    return {
        "status": "ok",
        "description": "Login correcto.",
        "jwt": access_token,
        "usuario": user,
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="jwt")
    response.delete_cookie(key="usuario")
    return {"status": "ok", "message": "Logout correcto."}


@router.get("/me")
async def current_user(usuario: EsteUsuario) -> UsuarioOut:
    return usuario


@router.get("/me/menu")
async def menues(usuario: EsteUsuario) -> str:
    return usuario.rol.menues
