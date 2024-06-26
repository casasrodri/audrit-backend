from controllers import BaseController
from database import SqlDB
from fastapi import HTTPException, status
from models import ResultadoBusquedaGlobal
from sqlalchemy import func
from utils.helpers import hash_string

from .model import UsuarioCreacion
from .schema import RolUsuarioDB, UsuarioDB


class CredencialesException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
        )


class UsuariosController(BaseController):
    async def get_all(db: SqlDB):
        return db.query(UsuarioDB).all()

    async def create(db: SqlDB, usuario: UsuarioCreacion):
        rol = (
            db.query(RolUsuarioDB)
            .filter(RolUsuarioDB.nombre == usuario.rol_nombre)
            .first()
        )

        if rol is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado",
            )

        email_existe = (
            db.query(UsuarioDB).filter(UsuarioDB.email == usuario.email).first()
        )

        if email_existe:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email ya registrado",
            )

        db_usuario = UsuarioDB(
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            password=hash_string(usuario.password),
            rol=rol,
        )

        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)

        return db_usuario

    async def validar_credenciales(user: UsuarioDB, password: str):
        if user.password != hash_string(password):
            raise CredencialesException()

    async def get_by_id(db: SqlDB, id: int):
        usuario = db.query(UsuarioDB).get(id)

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        return usuario

    async def get_by_email(db: SqlDB, email: str):
        usuario = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        return usuario

    async def buscar(db: SqlDB, texto_buscado: str):
        return (
            db.query(UsuarioDB)
            .filter(
                UsuarioDB.nombre.ilike(f"%{texto_buscado}%")
                | UsuarioDB.apellido.ilike(f"%{texto_buscado}%")
                | UsuarioDB.email.ilike(f"%{texto_buscado}%")
            )
            .all()
        )

    # async def update(usuario: UsuarioOut):
    #     return usuario

    # async def delete(id: int):
    #     return True

    async def buscar_global(db: SqlDB, texto: str):
        encontrados = (
            db.query(UsuarioDB)
            .filter(
                func.concat(UsuarioDB.nombre, " ", UsuarioDB.apellido).ilike(
                    f"%{texto}%"
                )
            )
            .all()
        )

        out = set()
        for user in encontrados:
            out.add(
                ResultadoBusquedaGlobal(
                    nombre=f"{user.nombre} {user.apellido}",
                    texto=f"{user.rol.nombre} - {user.email}",
                    tipo="usuario",
                    objeto={
                        "email": user.email,
                    },
                )
            )

        return list(out)[:10]
