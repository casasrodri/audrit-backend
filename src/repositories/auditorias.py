from .base import BaseRepository
from database.schemas.auditorias import AuditoriaSchema
from models.auditorias import AuditoriaCreacion
from fastapi import HTTPException, status


class AuditoriasRepo(BaseRepository):
    def get(self, sigla: str = None, id: int = None):

        tabla = self.db.query(AuditoriaSchema)

        if sigla:
            tabla = tabla.filter(AuditoriaSchema.sigla == sigla)

        if id:
            tabla = tabla.filter(AuditoriaSchema.id == id)

        return tabla.first()

    def get_all(self):
        return self.db.query(AuditoriaSchema).all()

    def create(self, auditoria: AuditoriaCreacion):
        db_aud = AuditoriaSchema(**auditoria.__dict__)

        if self.get(auditoria.sigla):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una auditoría con la sigla '{auditoria.sigla}'",
            )

        self.db.add(db_aud)
        self.db.commit()
        self.db.refresh(db_aud)

        return db_aud
