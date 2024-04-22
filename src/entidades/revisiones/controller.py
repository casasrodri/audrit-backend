from fastapi import HTTPException
from controllers import BaseController
from database import SqlDB
from .repo import RevisionesRepo
from .model import (
    RevisionCreacion,
    RevisionNodo,
    RevisionNodoData,
    RevisionActualizacion,
)


class RevisionesController(BaseController):
    def get_all(db: SqlDB):
        return RevisionesRepo(db).get_all()

    def get_all_auditoria(db: SqlDB, auditoria_id: int):
        revisiones = RevisionesRepo(db).get_all_auditoria(auditoria_id)
        return revisiones

    def get_nodos(db: SqlDB, auditoria_id: int):
        revisiones = RevisionesRepo(db).get_all_auditoria(auditoria_id)

        def crear_nodo(revision):
            data = RevisionNodoData(
                id=revision.id,
                sigla=revision.sigla,
                nombre=revision.nombre,
                descripcion=revision.descripcion,
                estado=revision.estado,
                informe=revision.informe,
                padre=revision.padre_id,
            )

            return RevisionNodo(
                key=revision.id,
                label=revision.nombre,
                data=data,
                children=[],
            )

        nodos = {revision.id: crear_nodo(revision) for revision in revisiones}

        for nodo in nodos.copy().values():
            if nodo.data.padre:
                id_padre = nodo.data.padre
                nodos[id_padre].children.append(nodo)

        out = [nodo for nodo in nodos.values() if nodo.data.padre is None]
        return out

    def create(db: SqlDB, revision: RevisionCreacion):
        return RevisionesRepo(db).create(revision)

    def update(db: SqlDB, id: int, revision: RevisionActualizacion):
        return RevisionesRepo(db).update(id, revision)

    def get(db: SqlDB, id: int):
        revision = RevisionesRepo(db).get(id)

        if revision is None:
            raise HTTPException(status_code=404, detail="Revision no encontrada.")

        return revision

    def delete(db: SqlDB, id: int):
        revision = RevisionesRepo(db).delete(id)

        if revision is None:
            raise HTTPException(status_code=404, detail="Revision no encontrado")

        return revision
