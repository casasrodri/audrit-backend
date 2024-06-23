from fastapi import HTTPException
from controllers import BaseController
from database import SqlDB
from entidades.relevamientos.schema import RelevamientoDB
from entidades.relevamientos.model import (
    RelevamientoCreacion,
    RelevamientoNodo,
    RelevamientoNodoData,
    RelevamientoActualizacion,
)
from entidades.documentos.schema import DocumentoDB
from utils.helpers import extraer_medio, editorjs_to_text
from entidades.revisiones.controller import RevisionesController
from models import ResultadoBusquedaGlobal


class RelevamientosController(BaseController):
    async def get_all(db: SqlDB):
        return db.query(RelevamientoDB).all()

    async def get_all_by_revision(db: SqlDB, revision_id: int):
        return (
            db.query(RelevamientoDB)
            .filter(RelevamientoDB.revision_id == revision_id)
            .all()
        )

    async def get_nodos_by_revision(
        db: SqlDB, revision_id: int, solo_agrupadores: bool = False
    ):
        relevamientos = await RelevamientosController.get_all_by_revision(
            db, revision_id
        )

        if solo_agrupadores:
            relevamientos = [
                relev for relev in relevamientos if relev.tipo != "documento"
            ]

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

    async def create(db: SqlDB, revision_id: int, relevamiento: RelevamientoCreacion):
        db_revision = await RevisionesController.get(db, revision_id)

        db_relevamiento = RelevamientoDB(
            tipo=relevamiento.tipo,
            revision_id=db_revision.id,
            sigla=relevamiento.sigla,
            nombre=relevamiento.nombre,
            padre_id=relevamiento.padre_id,
        )

        db.add(db_relevamiento)
        db.commit()
        db.refresh(db_relevamiento)

        # Creación del documento asociado
        from entidades.documentos.controller import DocumentosController
        from entidades.documentos.model import DocumentoCreacion

        documento = DocumentoCreacion(
            relevamiento_id=db_relevamiento.id, contenido="{}"
        )
        await DocumentosController.create(db, documento)

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

    async def buscar_global(db: SqlDB, texto: str):
        out = []
        out += await RelevamientosController._buscar_global_relevamientos(db, texto)
        out += await RelevamientosController._buscar_global_documentos(db, texto)
        return set(out)

    async def _buscar_global_relevamientos(
        db: SqlDB, texto: str
    ) -> list[ResultadoBusquedaGlobal]:
        # print("Se buscó en relevamientos.")

        encontrados = (
            db.query(RelevamientoDB)
            .filter(
                (RelevamientoDB.nombre.ilike(f"%{texto}%"))
                & (RelevamientoDB.tipo != "documento")
            )
            .all()
        )

        out = set()
        for relev in encontrados:
            revision = relev.revision
            auditoria = revision.auditoria

            out.add(
                ResultadoBusquedaGlobal(
                    nombre=relev.nombre,
                    texto=f"Revisión: {revision.nombre}",
                    tipo="revision",
                    objeto={
                        "siglaAudit": auditoria.sigla,
                        "siglaRev": revision.sigla,
                    },
                )
            )

        # print(out)
        return out

    async def _buscar_global_documentos(
        db: SqlDB, texto: str
    ) -> list[ResultadoBusquedaGlobal]:
        # print("Se buscó en documentos.")

        encontrados = (
            db.query(DocumentoDB)
            .join(RelevamientoDB)
            .filter(
                (RelevamientoDB.nombre.ilike(f"%{texto}%"))
                | (DocumentoDB.contenido.ilike(f"%{texto}%"))
            )
            .all()
        )

        out = set()
        for doc in encontrados:
            relev = doc.relevamiento
            revision = relev.revision
            auditoria = revision.auditoria
            # -------------------------------
            nombre = relev.nombre.replace("\n", " ").lower()
            contenido = editorjs_to_text(doc.contenido)

            def agregar(encontrado: str = None):
                if len(contenido) > 77:
                    descr = contenido[:77] + "..."
                else:
                    descr = contenido

                out.add(
                    ResultadoBusquedaGlobal(
                        nombre=relev.nombre,
                        texto=encontrado or descr,
                        tipo="documento",
                        objeto={
                            "siglaAudit": auditoria.sigla,
                            "siglaRev": revision.sigla,
                            "relevId": relev.id,
                        },
                    )
                )

            contenido = contenido.replace("\n", " ").lower()
            texto = texto.lower()
            if texto in contenido:
                subtextos = extraer_medio(texto, contenido)
                for sub in subtextos:
                    agregar(sub)
            elif texto in nombre:
                agregar()

        # print(out)
        return out
