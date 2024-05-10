from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .schema import DocumentoSchema
from .model import (
    DocumentoCreacion,
    DocumentoActualizacion,
)


class DocumentosController(BaseController):
    def get_all(db: SqlDB):
        return db.query(DocumentoSchema).all()

    def get_by_relevamiento(db: SqlDB, relevamiento_id: int):
        documento = (
            db.query(DocumentoSchema)
            .filter(DocumentoSchema.relevamiento_id == relevamiento_id)
            .first()
        )

        if documento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado"
            )

        return documento

    def create(db: SqlDB, documento: DocumentoCreacion):
        db_documento = DocumentoSchema(
            relevamiento_id=documento.relevamiento_id,
            contenido=documento.contenido,
        )

        db.add(db_documento)
        db.commit()
        db.refresh(db_documento)

        return db_documento

    def update(db: SqlDB, id: int, documento: DocumentoActualizacion):
        db_documento = DocumentosController.get(db, id)

        db_documento.relevamiento_id = documento.relevamiento_id
        db_documento.contenido = documento.contenido

        db.commit()
        db.refresh(db_documento)

        return db_documento

    def get(db: SqlDB, id: int):
        documento = db.query(DocumentoSchema).filter(DocumentoSchema.id == id).first()

        if documento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado"
            )

        return documento

    def delete(db: SqlDB, id: int):
        db_documento = DocumentosController.get(db, id)

        print("Objeto encontrado: ", db_documento)

        db.delete(db_documento)
        db.commit()

        return db_documento
