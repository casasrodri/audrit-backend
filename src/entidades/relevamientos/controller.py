from fastapi import HTTPException
from controllers import BaseController
from database import SqlDB
from .schema import RelevamientoDB
from .model import (
    RelevamientoCreacion,
    RelevamientoNodo,
    RelevamientoNodoData,
    RelevamientoActualizacion,
)


class RelevamientosController(BaseController):
    async def get_all(db: SqlDB):
        return db.query(RelevamientoDB).all()

    async def get_all_by_revision(db: SqlDB, revision_id: int):
        return (
            db.query(RelevamientoDB)
            .filter(RelevamientoDB.revision_id == revision_id)
            .all()
        )

    async def get_nodos_by_revision(db: SqlDB, revision_id: int):
        relevamientos = await RelevamientosController.get_all_by_revision(
            db, revision_id
        )

        def crear_nodo(relevamiento):
            data = RelevamientoNodoData(
                id=relevamiento.id,
                tipo=relevamiento.tipo,
                revision=relevamiento.revision_id,
                sigla=relevamiento.sigla,
                nombre=relevamiento.nombre,
                padre=relevamiento.padre_id,
            )

            return RelevamientoNodo(
                key=relevamiento.id,
                label=relevamiento.nombre,
                data=data,
                children=[],
            )

        nodos = {
            relevamiento.id: crear_nodo(relevamiento) for relevamiento in relevamientos
        }

        for nodo in nodos.copy().values():
            if nodo.data.padre:
                id_padre = nodo.data.padre
                nodos[id_padre].children.append(nodo)

        out = [nodo for nodo in nodos.values() if nodo.data.padre is None]
        return out

    async def create(db: SqlDB, relevamiento: RelevamientoCreacion):
        db_relevamiento = RelevamientoDB(
            sigla=relevamiento.sigla,
            nombre=relevamiento.nombre,
            descripcion=relevamiento.descripcion,
            padre_id=relevamiento.padre_id,
        )

        db.add(db_relevamiento)
        db.commit()
        db.refresh(db_relevamiento)

        return db_relevamiento

    async def update(db: SqlDB, id: int, relevamiento: RelevamientoActualizacion):
        db_relevamiento = await RelevamientosController.get(db, id)

        db_relevamiento.sigla = relevamiento.sigla
        db_relevamiento.nombre = relevamiento.nombre
        db_relevamiento.descripcion = relevamiento.descripcion
        db_relevamiento.padre_id = relevamiento.padre_id

        db.commit()
        db.refresh(db_relevamiento)

        return db_relevamiento

    async def get(db: SqlDB, id: int, links: bool = True):
        relevamiento = db.query(RelevamientoDB).get(id)

        if relevamiento is None:
            raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

        # Obtención de links
        if links:
            from entidades.links.controller import LinksController, EntidadLinkeable

            relevamiento.links = await LinksController.get(
                db, EntidadLinkeable.relevamiento, id
            )

        return relevamiento

    async def delete(db: SqlDB, id: int):
        db_relevamiento = await RelevamientosController.get(db, id)
        print("Objeto encontrado: ", db_relevamiento)

        db.delete(db_relevamiento)
        db.commit()

        return db_relevamiento
