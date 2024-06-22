from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .model import RiesgoCreacion, RiesgoActualizacion
from .schema import RiesgoDB
from entidades.revisiones.controller import RevisionesController
from models import ResultadoBusquedaGlobal
from utils.helpers import extraer_medio


class RiesgosController(BaseController):
    async def get_all(db: SqlDB):
        return db.query(RiesgoDB).all()

    async def get_all_by_revision(db: SqlDB, revision_id: int):
        return db.query(RiesgoDB).filter(RiesgoDB.revision_id == revision_id).all()

    async def create(db: SqlDB, riesgo: RiesgoCreacion):
        revision = await RevisionesController.get(db, riesgo.revision_id)
        print("riesgo recibido:", riesgo)
        print(
            f"♯4c1d7d → ({revision.__class__.__module__}.{revision.__class__.__name__}) revision =",
            revision,
        )

        db_riesgo = RiesgoDB(
            nombre=riesgo.nombre,
            descripcion=riesgo.descripcion,
            nivel=riesgo.nivel,
            revision=revision,
        )

        db.add(db_riesgo)
        db.commit()
        db.refresh(db_riesgo)

        from entidades.links.controller import (
            LinksController,
            EntidadLinkeable,
        )

        for oc in riesgo.objetivos_control:
            await LinksController.create(
                db,
                EntidadLinkeable.riesgo,
                db_riesgo.id,
                EntidadLinkeable.objetivo_control,
                oc,
            )

        return db_riesgo

    async def update(db: SqlDB, id: int, riesgo: RiesgoActualizacion):
        db_riesgo = await RiesgosController.get(db, id)

        db_riesgo.nombre = riesgo.nombre
        db_riesgo.descripcion = riesgo.descripcion
        db_riesgo.nivel = riesgo.nivel

        from entidades.links.controller import (
            LinksController,
            EntidadLinkeable,
        )

        # Se eliminan los links de objetivos de control
        await LinksController.delete_all_objetivos_control(db, id)

        # Se crean nuevamente todas las asociaciones
        for oc in riesgo.objetivos_control:
            await LinksController.create(
                db,
                EntidadLinkeable.riesgo,
                id,
                EntidadLinkeable.objetivo_control,
                oc,
            )

        db.commit()
        db.refresh(db_riesgo)

        return db_riesgo

    async def get(db: SqlDB, id: int, links: bool = True):
        riesgo = db.query(RiesgoDB).get(id)

        if riesgo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Riesgo no encontrado"
            )

        # Obtención de links
        if links:
            from entidades.links.controller import LinksController, EntidadLinkeable

            riesgo.links = await LinksController.get(db, EntidadLinkeable.riesgo, id)

        return riesgo

    async def buscar(db: SqlDB, revision_id: int, texto_buscado: str):
        return (
            db.query(RiesgoDB)
            .filter(RiesgoDB.revision_id == revision_id)
            .filter(
                RiesgoDB.nombre.ilike(f"%{texto_buscado}%")
                | RiesgoDB.descripcion.ilike(f"%{texto_buscado}%")
            )
            .all()
        )

    # def delete(db: SqlDB, id: int):
    #     riesgo = RiesgoRepo(db).delete(id)

    #     if riesgo is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return riesgo

    async def buscar_global(db: SqlDB, texto: str):
        encontrados = (
            db.query(RiesgoDB)
            .filter(
                RiesgoDB.nombre.ilike(f"%{texto}%")
                | RiesgoDB.descripcion.ilike(f"%{texto}%")
            )
            .all()
        )

        out = set()
        for rie in encontrados:
            rev = rie.revision
            aud = rev.auditoria

            def agregar(encontrado: str = None):
                if len(rie.descripcion) > 77:
                    descr = rie.descripcion[:77] + "..."
                else:
                    descr = rie.descripcion

                out.add(
                    ResultadoBusquedaGlobal(
                        nombre=f"{rie.nombre} ({rie.nivel})",
                        texto=encontrado or descr,
                        tipo="riesgo",
                        objeto={
                            "siglaAudit": aud.sigla,
                            "siglaRev": rev.sigla,
                            "id": rie.id,
                        },
                    )
                )

            # Variables
            buscar = texto.replace("\n", " ").lower()
            descripcion = rie.descripcion.replace("\n", " ").lower()

            # Agregación de coincidencias
            if buscar in descripcion:
                subtextos = extraer_medio(buscar, descripcion)
                for sub in subtextos:
                    agregar(sub)
            else:
                agregar()

        return out
