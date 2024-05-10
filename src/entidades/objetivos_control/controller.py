from fastapi import HTTPException
from controllers import BaseController
from database import SqlDB
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

    def get(db: SqlDB, id: int):
        objetivo = db.query(ObjetivoControlDB).get(id)

        if objetivo is None:
            raise HTTPException(
                status_code=404, detail="Objetivo de control no encontrado"
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
