from controllers import BaseController
from database import SqlDB
from fastapi import HTTPException

from .model import ObjetivoControlCreacion
from .schema import ObjetivoControlDB


class ObjetivosControlController(BaseController):
    def get_all(db: SqlDB):
        return db.query(ObjetivoControlDB).all()

    def create(db: SqlDB, objetivo: ObjetivoControlCreacion):
        db_objetivo = ObjetivoControlDB(
            nombre=objetivo.nombre,
            descripcion=objetivo.descripcion,
        )

        db.add(db_objetivo)
        db.commit()
        db.refresh(db_objetivo)

        return db_objetivo

    async def get(db: SqlDB, id: int, links: bool = False):
        objetivo = db.query(ObjetivoControlDB).get(id)

        if objetivo is None:
            raise HTTPException(
                status_code=404, detail="Objetivo de control no encontrado"
            )

        # Obtención de links
        if links:
            from entidades.links.controller import EntidadLinkeable, LinksController

            objetivo.links = await LinksController.get(
                db, EntidadLinkeable.objetivo_control, id
            )

        return objetivo

    def delete(db: SqlDB, id: int):
        db_objetivo = ObjetivosControlController.get(db, id)

        print("Objeto encontrado: ", db_objetivo)

        db.delete(db_objetivo)
        db.commit()

        return db_objetivo

    # def update(db: SqlDB, id: int, objetivo: RelevamientoActualizacion):
    #     return ObjetivoControlRepo(db).update(id, objetivo)
