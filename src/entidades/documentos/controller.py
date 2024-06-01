from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .schema import DocumentoDB
from .model import (
    DocumentoCreacion,
    DocumentoActualizacion,
)
from json import loads
from entidades.links.controller import LinksController, EntidadLinkeable, CONTROLLERS
from datetime import datetime


async def buscar_objetos(
    tipo: str, blocks: list, controlador: BaseController, db: SqlDB
) -> list:
    out = []
    ids = {b["data"]["id"] for b in blocks if b["type"] == tipo}

    for id in ids:
        try:
            out.append(await controlador.get(db, id))
        except:
            ...

    return out


async def asociar(
    tipo: EntidadLinkeable, documento: DocumentoDB, blocks: list, db: SqlDB
):
    controller = CONTROLLERS[tipo]
    obj_asociados = await buscar_objetos(tipo.name, blocks, controller, db)

    for obj in obj_asociados:
        await LinksController.create(
            db, EntidadLinkeable.relevamiento, documento.relevamiento_id, tipo, obj.id
        )


class DocumentosController(BaseController):
    async def get_all(db: SqlDB) -> list[DocumentoDB]:
        return db.query(DocumentoDB).all()

    async def get_by_relevamiento(db: SqlDB, relevamiento_id: int) -> list[DocumentoDB]:
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

    async def create(db: SqlDB, documento: DocumentoCreacion) -> DocumentoDB:
        db_documento = DocumentoDB(
            relevamiento_id=documento.relevamiento_id,
            contenido=documento.contenido,
        )

        db.add(db_documento)
        db.commit()
        db.refresh(db_documento)

        return db_documento

    async def update(
        db: SqlDB, id: int, documento: DocumentoActualizacion
    ) -> DocumentoDB:
        db_documento = await DocumentosController.get(db, id)

        db_documento.contenido = documento.contenido

        # Se analiza los elementos linkeados
        blocks = loads(documento.contenido)["blocks"]

        # Se eliminan las asociaciones anteriores
        await LinksController.delete_all_links(db, db_documento.relevamiento_id)

        # Se generan las asociaciones nuevamente
        await asociar(EntidadLinkeable.riesgo, db_documento, blocks, db)
        await asociar(EntidadLinkeable.control, db_documento, blocks, db)
        await asociar(EntidadLinkeable.normativa, db_documento, blocks, db)
        await asociar(EntidadLinkeable.organigrama, db_documento, blocks, db)
        await asociar(EntidadLinkeable.aplicacion, db_documento, blocks, db)

        db_documento.actualizacion = datetime.now()

        db.commit()
        db.refresh(db_documento)

        return db_documento

    async def get(db: SqlDB, id: int, links: bool = True) -> DocumentoDB:
        documento = db.query(DocumentoDB).filter(DocumentoDB.id == id).first()

        if documento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado"
            )

        if links:
            from entidades.links.controller import LinksController, EntidadLinkeable

            documento.links = await LinksController.get(
                db, EntidadLinkeable.relevamiento, documento.relevamiento_id
            )

        return documento

    async def delete(db: SqlDB, id: int) -> DocumentoDB:
        db_documento = DocumentosController.get(db, id)

        print("Objeto encontrado: ", db_documento)

        db.delete(db_documento)
        db.commit()

        return db_documento
