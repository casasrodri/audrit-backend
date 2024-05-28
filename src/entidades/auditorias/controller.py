from controllers import BaseController
from fastapi import HTTPException, status
from database import SqlDB
from .model import AuditoriaCreacion
from models import ResultadoBusquedaGlobal

from .schema import AuditoriaDB


class AuditoriasController(BaseController):
    def get_all(db: SqlDB):
        return db.query(AuditoriaDB).all()

    def get(db: SqlDB, sigla: str = None, id: int = None):
        tabla = db.query(AuditoriaDB)

        if sigla:
            tabla = tabla.filter(AuditoriaDB.sigla == sigla)

        if id:
            tabla = tabla.filter(AuditoriaDB.id == id)

        auditoria = tabla.first()

        if not auditoria:
            raise HTTPException(status_code=404, detail="Auditoria no encontrada")

        return auditoria

    def get_by_sigla(db: SqlDB, sigla: str):
        return AuditoriasController.get(db, sigla=sigla)

    def get_by_id(db: SqlDB, id: int):
        return AuditoriasController.get(db, id=id)

    def create(db: SqlDB, auditoria: AuditoriaCreacion):
        db_aud = AuditoriaDB(**auditoria.__dict__)

        if AuditoriasController.get(db, sigla=auditoria.sigla):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una auditoría con la sigla '{auditoria.sigla}'",
            )

        db.add(db_aud)
        db.commit()
        db.refresh(db_aud)

        return db_aud

    async def buscar_global(db: SqlDB, texto: str):
        encontrados = (
            db.query(AuditoriaDB)
            .filter(
                AuditoriaDB.sigla.ilike(f"%{texto}%")
                | AuditoriaDB.nombre.ilike(f"%{texto}%")
                | AuditoriaDB.tipo.ilike(f"%{texto}%")
            )
            .all()
        )

        print(encontrados)

        out = []
        for rtdo in encontrados:
            texto = f"{rtdo.sigla} - {rtdo.nombre} - {rtdo.tipo}"
            out.append(
                ResultadoBusquedaGlobal(
                    nombre=rtdo.nombre,
                    texto=texto,
                    objeto="auditoria",
                    objeto_id=rtdo.id,
                )
            )

        return out
