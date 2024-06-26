from controllers import BaseController
from fastapi import HTTPException, status
from database import SqlDB
from entidades.auditorias.model import AuditoriaCreacion
from models import ResultadoBusquedaGlobal
from sqlalchemy import desc

from .schema import AuditoriaDB


class AuditoriasController(BaseController):
    def get_all(db: SqlDB):
        return db.query(AuditoriaDB).order_by(desc(AuditoriaDB.id)).all()

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
        db_aud = AuditoriaDB(
            sigla=auditoria.sigla,
            nombre=auditoria.nombre,
            tipo=auditoria.tipo,
            estado=auditoria.estado,
            periodo=auditoria.periodo,
        )

        try:
            existente = AuditoriasController.get(db, sigla=auditoria.sigla)
        except HTTPException:
            existente = None

        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una auditoría con la sigla '{auditoria.sigla}'",
            )

        db.add(db_aud)
        db.commit()
        db.refresh(db_aud)

        return db_aud

    def update(db: SqlDB, id: int, auditoria: AuditoriaCreacion):
        db_aud = AuditoriasController.get(db, id=id)

        db_aud.sigla = auditoria.sigla
        db_aud.nombre = auditoria.nombre
        db_aud.tipo = auditoria.tipo
        db_aud.estado = auditoria.estado
        db_aud.periodo = auditoria.periodo

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

        out = set()
        for audit in encontrados:
            texto = f"{audit.sigla} - {audit.nombre} - {audit.tipo}"
            out.add(
                ResultadoBusquedaGlobal(
                    nombre=audit.nombre,
                    texto=texto,
                    tipo="auditoria",
                    objeto={"siglaAudit": audit.sigla},
                )
            )

        return out[:10]
