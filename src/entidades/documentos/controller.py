from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .schema import DocumentoDB
from .model import (
    DocumentoCreacion,
    DocumentoActualizacion,
)
from json import loads
from entidades.riesgos.controller import RiesgosController
from entidades.riesgos.schema import RiesgoDB


def buscar_objetos(
    tipo: str, blocks: list, controlador: BaseController, db: SqlDB
) -> list:
    out = []
    ids = {b["data"]["id"] for b in blocks if b["type"] == tipo}

    for id in ids:
        try:
            out.append(controlador.get(db, id))
        except:
            ...

    return out


def asociar_riesgos(documento: DocumentoDB, blocks: list, db: SqlDB):
    obj_asociados = buscar_objetos("riesgo", blocks, RiesgosController, db)

    # Se incorporan asociaciones:
    ries: RiesgoDB
    for ries in obj_asociados:
        if ries not in documento.riesgos:
            documento.riesgos.append(ries)

        if documento not in ries.documentos:
            ries.documentos.append(documento)

    # Se eliminan los que no están más:
    eliminar = set(documento.riesgos) - set(obj_asociados)

    for ries in eliminar:
        if ries in documento.riesgos:
            documento.riesgos.remove(ries)
        if documento in ries.documentos:
            ries.documentos.remove(documento)


class DocumentosController(BaseController):
    def get_all(db: SqlDB):
        return db.query(DocumentoDB).all()

    def get_by_relevamiento(db: SqlDB, relevamiento_id: int):
        documento = (
            db.query(DocumentoDB)
            .filter(DocumentoDB.relevamiento_id == relevamiento_id)
            .first()
        )

        if documento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado"
            )

        return documento

    def create(db: SqlDB, documento: DocumentoCreacion):
        db_documento = DocumentoDB(
            relevamiento_id=documento.relevamiento_id,
            contenido=documento.contenido,
        )

        db.add(db_documento)
        db.commit()
        db.refresh(db_documento)

        return db_documento

    def update(db: SqlDB, id: int, documento: DocumentoActualizacion):
        db_documento: DocumentoDB = DocumentosController.get(db, id)

        db_documento.relevamiento_id = documento.relevamiento_id
        db_documento.contenido = documento.contenido

        # Se analiza los elementos linkeados
        blocks = loads(documento.contenido)["blocks"]

        # Se generan las asociaciones
        asociar_riesgos(db_documento, blocks, db)

        db.commit()
        db.refresh(db_documento)

        return db_documento

    def get(db: SqlDB, id: int):
        documento = db.query(DocumentoDB).filter(DocumentoDB.id == id).first()

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
