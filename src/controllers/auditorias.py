from .base import BaseController
from fastapi import HTTPException
from database.base import SqlDB
from repositories.auditorias import AuditoriasRepo
from models.auditorias import AuditoriaCreacion


class AuditoriasController(BaseController):
    def get_all(db: SqlDB):
        return AuditoriasRepo(db).get_all()

    def get(db: SqlDB, sigla: str = None, id: int = None):
        auditoria = AuditoriasRepo(db).get(sigla, id)

        if not auditoria:
            raise HTTPException(status_code=404, detail="Auditoria no encontrada")

        return auditoria

    def get_by_sigla(db: SqlDB, sigla: str):
        return AuditoriasController.get(db, sigla=sigla)

    def get_by_id(db: SqlDB, id: int):
        return AuditoriasController.get(db, id=id)

    def create(db: SqlDB, auditoria: AuditoriaCreacion):
        return AuditoriasRepo(db).create(auditoria)
