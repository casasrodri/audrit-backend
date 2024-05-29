from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .schema import UsuarioDB, RolUsuarioDB
from .model import UsuarioOut, UsuarioCreacion
from models import ResultadoBusquedaGlobal
from sqlalchemy import func


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
            # TODO hash password
            email=usuario.email,
            password=usuario.password,
            rol=rol,
        )

        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)

        return db_usuario

    async def validar_credenciales(db: SqlDB, email: str, password: str) -> bool:
        usuario = await UsuariosController.get_by_email(db, email)
        return usuario.password == password

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

        return out
