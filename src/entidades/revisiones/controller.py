from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .schema import RevisionDB
from .model import (
    RevisionCreacion,
    RevisionNodo,
    RevisionNodoData,
    RevisionActualizacion,
)
from models import ResultadoBusquedaGlobal
from utils.helpers import extraer_medio
from entidades.auditorias.controller import AuditoriasController


class RevisionesController(BaseController):
    async def get_all(db: SqlDB):
        return db.query(RevisionDB).all()

    async def get_all_auditoria(db: SqlDB, auditoria_id: int):
        revisiones = (
            db.query(RevisionDB).filter(RevisionDB.auditoria_id == auditoria_id).all()
        )

        return revisiones

    async def get_nodos(db: SqlDB, auditoria_id: int):
        revisiones = await RevisionesController.get_all_auditoria(db, auditoria_id)

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

    async def create(db: SqlDB, auditoria_id: int, revision: RevisionCreacion):
        db_audit = AuditoriasController.get(db, id=auditoria_id)

        db_revision = RevisionDB(
            auditoria_id=db_audit.id,
            sigla=revision.sigla,
            nombre=revision.nombre,
            descripcion=revision.descripcion,
            padre_id=revision.padre_id,
            estado="pendiente",
        )

        db.add(db_revision)
        db.commit()
        db.refresh(db_revision)

        return db_revision

    async def update(db: SqlDB, id: int, revision: RevisionActualizacion):
        db_revision = await RevisionesController.get(db, id)

        db_revision.sigla = revision.sigla
        db_revision.nombre = revision.nombre
        db_revision.descripcion = revision.descripcion
        db_revision.padre_id = revision.padre_id

        db.commit()
        db.refresh(db_revision)

        return db_revision

    async def get(db: SqlDB, id: int):
        revision = db.query(RevisionDB).get(id)

        if revision is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Revision no encontrada."
            )

        return revision

    async def delete(db: SqlDB, id: int):
        db_revision = RevisionesController.get(db, id)

        print("Objeto encontrado: ", db_revision)

        db.delete(db_revision)
        db.commit()

        return db_revision

    async def buscar_global(db: SqlDB, texto: str):
        encontrados = (
            db.query(RevisionDB)
            .filter(
                (RevisionDB.nombre.ilike(f"%{texto}%"))
                | (RevisionDB.descripcion.ilike(f"%{texto}%"))
            )
            .all()
        )

        out = set()
        for revi in encontrados:
            nombre = revi.nombre.replace("\n", " ").lower()
            descrip = revi.descripcion.replace("\n", " ").lower()

            def agregar(encontrado: str = None):
                descr = f"Auditoría: {revi.auditoria.nombre} - {revi.descripcion}"
                if len(descr) > 77:
                    descr = descr[:77] + "..."
                else:
                    descr = descr

                out.add(
                    ResultadoBusquedaGlobal(
                        nombre=revi.nombre,
                        texto=encontrado or descr,
                        tipo="revision",
                        objeto={
                            "siglaAudit": revi.auditoria.sigla,
                            "siglaRev": revi.sigla,
                        },
                    )
                )

            if texto in descrip:
                subtextos = extraer_medio(texto, descrip)
                for sub in subtextos:
                    agregar(sub)
            elif texto in nombre:
                agregar()

        return out[:10]
