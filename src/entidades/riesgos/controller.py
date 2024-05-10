from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .model import RiesgoCreacion, RiesgoActualizacion
from .schema import RiesgoSchema
from entidades.revisiones.controller import RevisionesController
from entidades.objetivos_control.controller import ObjetivosControlController


class RiesgosController(BaseController):
    def get_all(db: SqlDB):
        return db.query(RiesgoSchema).all()

    def get_all_by_revision(db: SqlDB, revision_id: int):
        return (
            db.query(RiesgoSchema).filter(RiesgoSchema.revision_id == revision_id).all()
        )

    def create(db: SqlDB, riesgo: RiesgoCreacion):
        # revision = db.query(RevisionSchema).get(riesgo.revision_id)
        revision = RevisionesController.get(db, riesgo.revision_id)

        db_riesgo = RiesgoSchema(
            nombre=riesgo.nombre,
            descripcion=riesgo.descripcion,
            nivel=riesgo.nivel,
            revision=revision,
        )

        db_riesgo.objetivos_control = [
            # db.query(ObjetivoControlSchema).get(objetivo_id)
            ObjetivosControlController.get(db, objetivo_id)
            for objetivo_id in riesgo.objetivos_control
        ]

        db.add(db_riesgo)
        db.commit()
        db.refresh(db_riesgo)

        return db_riesgo

    def update(db: SqlDB, id: int, riesgo: RiesgoActualizacion):
        db_riesgo = RiesgosController.get(db, id)

        db_riesgo.nombre = riesgo.nombre
        db_riesgo.descripcion = riesgo.descripcion
        db_riesgo.nivel = riesgo.nivel

        db_riesgo.objetivos_control = [
            # db.query(ObjetivoControlSchema).get(objetivo_id)
            ObjetivosControlController.get(db, objetivo_id)
            for objetivo_id in riesgo.objetivos_control
        ]

        db.commit()
        db.refresh(db_riesgo)

        return db_riesgo

    def get(db: SqlDB, id: int):
        riesgo = db.query(RiesgoSchema).get(id)

        if riesgo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Riesgo no encontrado"
            )

        return riesgo

    def buscar(db: SqlDB, revision_id: int, texto_buscado: str):
        return (
            db.query(RiesgoSchema)
            .filter(RiesgoSchema.revision_id == revision_id)
            .filter(
                RiesgoSchema.nombre.ilike(f"%{texto_buscado}%")
                | RiesgoSchema.descripcion.ilike(f"%{texto_buscado}%")
            )
            .all()
        )

    # def delete(db: SqlDB, id: int):
    #     riesgo = RiesgoRepo(db).delete(id)

    #     if riesgo is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return riesgo
