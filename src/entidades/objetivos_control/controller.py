from fastapi import HTTPException
from controllers import BaseController
from database import SqlDB
from .repo import ObjetivoControlRepo
from .model import ObjetivoControlCreacion


class ObjetivoControlController(BaseController):
    def get_all(db: SqlDB):
        return ObjetivoControlRepo(db).get_all()

    def create(db: SqlDB, objetivo: ObjetivoControlCreacion):
        return ObjetivoControlRepo(db).create(objetivo)

    # def update(db: SqlDB, id: int, objetivo: RelevamientoActualizacion):
    #     return ObjetivoControlRepo(db).update(id, objetivo)

    # def get(db: SqlDB, id: int):
    #     objetivo = ObjetivoControlRepo(db).get(id)

    #     if objetivo is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return objetivo

    # def delete(db: SqlDB, id: int):
    #     objetivo = ObjetivoControlRepo(db).delete(id)

    #     if objetivo is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return objetivo
