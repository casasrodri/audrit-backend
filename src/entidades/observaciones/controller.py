from controllers import BaseController
from database import SqlDB
from fastapi import HTTPException, status
from models import ResultadoBusquedaGlobal
from utils.helpers import extraer_medio

from entidades.revisiones.controller import RevisionesController

from .model import ObservacionActualizacion, ObservacionCreacion
from .schema import ObservacionDB


class ObservacionesController(BaseController):
    async def get_all(db: SqlDB):  # OK
        return db.query(ObservacionDB).all()

    async def get_all_by_revision(db: SqlDB, revision_id: int):  # OK
        return (
            db.query(ObservacionDB)
            .filter(ObservacionDB.revision_id == revision_id)
            .all()
        )

    async def create(db: SqlDB, observacion: ObservacionCreacion):  # OK
        revision = await RevisionesController.get(db, observacion.revision_id)

        db_observacion = ObservacionDB(
            nombre=observacion.nombre,
            descripcion=observacion.descripcion,
            riesgo=observacion.riesgo,
            responsable=observacion.responsable,
            estado=observacion.estado,
            sector_auditoria=observacion.sector_auditoria,
            efectos=observacion.efectos,
            recomendaciones=observacion.recomendaciones,
            fecha_alta=observacion.fecha_alta,
            fecha_solucion=observacion.fecha_solucion,
            revision=revision,
        )

        db.add(db_observacion)
        db.commit()
        db.refresh(db_observacion)

        return db_observacion

    async def update(
        db: SqlDB, id: int, observacion: ObservacionActualizacion
    ):  # TODO Probar
        db_observacion = await ObservacionesController.get(db, id)

        db_observacion.nombre = observacion.nombre
        db_observacion.descripcion = observacion.descripcion
        db_observacion.riesgo = observacion.riesgo
        db_observacion.responsable = observacion.responsable
        db_observacion.estado = observacion.estado
        db_observacion.sector_auditoria = observacion.sector_auditoria
        db_observacion.efectos = observacion.efectos
        db_observacion.recomendaciones = observacion.recomendaciones
        db_observacion.fecha_solucion = observacion.fecha_solucion

        db.commit()
        db.refresh(db_observacion)

        return db_observacion

    async def get(db: SqlDB, id: int, links: bool = True):  # Ok
        observacion = db.query(ObservacionDB).get(id)

        if observacion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Observacion no encontrada",
            )

        # Obtención de links
        if links:
            from entidades.links.controller import EntidadLinkeable, LinksController

            observacion.links = await LinksController.get(
                db, EntidadLinkeable.observacion, id
            )

        return observacion

    async def buscar(db: SqlDB, revision_id: int, texto_buscado: str):
        return (
            db.query(ObservacionDB)
            .filter(ObservacionDB.revision_id == revision_id)
            .filter(
                ObservacionDB.nombre.ilike(f"%{texto_buscado}%")
                | ObservacionDB.descripcion.ilike(f"%{texto_buscado}%")
                | ObservacionDB.efectos.ilike(f"%{texto_buscado}%")
                | ObservacionDB.recomendaciones.ilike(f"%{texto_buscado}%")
            )
            .all()
        )

    # def delete(db: SqlDB, id: int):
    #     observacion = ObservacionRepo(db).delete(id)

    #     if observacion is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return observacion

    async def buscar_global(db: SqlDB, texto: str):
        encontrados = (
            db.query(ObservacionDB)
            .filter(
                ObservacionDB.nombre.ilike(f"%{texto}%")
                | ObservacionDB.descripcion.ilike(f"%{texto}%")
                | ObservacionDB.efectos.ilike(f"%{texto}%")
                | ObservacionDB.recomendaciones.ilike(f"%{texto}%")
            )
            .all()
        )

        out = set()
        for obs in encontrados:
            rev = obs.revision
            aud = rev.auditoria

            def agregar(encontrado: str = None):
                if len(obs.descripcion) > 77:
                    descr = obs.descripcion[:77] + "..."
                else:
                    descr = obs.descripcion

                out.add(
                    ResultadoBusquedaGlobal(
                        nombre=obs.nombre,
                        texto=encontrado or descr,
                        tipo="observacion",
                        objeto={
                            "siglaAudit": aud.sigla,
                            "siglaRev": rev.sigla,
                            "id": obs.id,
                        },
                    )
                )

            # Variables
            buscar = texto.replace("\n", " ").lower()
            nombre = obs.nombre.lower()
            descripcion = obs.descripcion.replace("\n", " ").lower()
            efectos = obs.efectos.replace("\n", " ").lower()
            recomendaciones = obs.recomendaciones.replace("\n", " ").lower()
            solo_nombre = True
            print("Procesando obs:", obs)

            # Agregación de coincidencias
            if buscar in descripcion:
                solo_nombre = False
                subtextos = extraer_medio(buscar, descripcion)
                for sub in subtextos:
                    agregar(sub)

            if buscar in efectos:
                solo_nombre = False
                subtextos = extraer_medio(buscar, efectos, longitud=70)
                for sub in subtextos:
                    agregar(f"Efectos: {sub}")

            if buscar in recomendaciones:
                solo_nombre = False
                subtextos = extraer_medio(buscar, recomendaciones, longitud=65)
                for sub in subtextos:
                    agregar(f"Recomendaciones: {sub}")

            if solo_nombre and buscar in nombre:
                agregar()

        return list(out)[:10]
