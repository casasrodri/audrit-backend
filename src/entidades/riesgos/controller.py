from fastapi import HTTPException
from controllers import BaseController
from database import SqlDB
from .repo import RelevamientosRepo
from .model import (
    RelevamientoCreacion,
    RelevamientoNodo,
    RelevamientoNodoData,
    RelevamientoActualizacion,
)


class RelevamientosController(BaseController):
    def get_all(db: SqlDB):
        return RelevamientosRepo(db).get_all()

    def get_nodos_by_revision(db: SqlDB, revision_id: int):
        relevamientos = RelevamientosRepo(db).get_all_by_revision(revision_id)

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

    def create(db: SqlDB, relevamiento: RelevamientoCreacion):
        return RelevamientosRepo(db).create(relevamiento)

    def update(db: SqlDB, id: int, relevamiento: RelevamientoActualizacion):
        return RelevamientosRepo(db).update(id, relevamiento)

    def get(db: SqlDB, id: int):
        relevamiento = RelevamientosRepo(db).get(id)

        if relevamiento is None:
            raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

        return relevamiento

    def delete(db: SqlDB, id: int):
        relevamiento = RelevamientosRepo(db).delete(id)

        if relevamiento is None:
            raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

        return relevamiento
