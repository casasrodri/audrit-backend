from fastapi import HTTPException
from controllers import BaseController
from database import SqlDB
from .repo import DocumentosRepo
from .model import (
    DocumentoCreacion,
    DocumentoActualizacion,
)


class DocumentosController(BaseController):
    def get_all(db: SqlDB):
        return DocumentosRepo(db).get_all()

    def get_by_relevamiento(db: SqlDB, relevamiento_id: int):
        documento = DocumentosRepo(db).get_by_relevamiento(relevamiento_id)

        if documento is None:
            raise HTTPException(status_code=404, detail="Documento no encontrado")

        return documento

    def create(db: SqlDB, documento: DocumentoCreacion):
        return DocumentosRepo(db).create(documento)

    def update(db: SqlDB, id: int, documento: DocumentoActualizacion):
        return DocumentosRepo(db).update(id, documento)

    def get(db: SqlDB, id: int):
        documento = DocumentosRepo(db).get(id)

        if documento is None:
            raise HTTPException(status_code=404, detail="Documento no encontrado")

        return documento

    def delete(db: SqlDB, id: int):
        documento = DocumentosRepo(db).delete(id)

        if documento is None:
            raise HTTPException(status_code=404, detail="Documento no encontrado")

        return documento
