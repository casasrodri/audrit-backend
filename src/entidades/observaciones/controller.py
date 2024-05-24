from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .model import ObservacionCreacion, ObservacionActualizacion
from .schema import ObservacionDB
from entidades.revisiones.controller import RevisionesController


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
            from entidades.links.controller import LinksController, EntidadLinkeable

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
