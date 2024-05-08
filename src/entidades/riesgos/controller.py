from fastapi import HTTPException
from controllers import BaseController
from database import SqlDB
from .repo import RiesgoRepo
from .model import RiesgoCreacion, RiesgoActualizacion


class RiesgoController(BaseController):
    def get_all(db: SqlDB):
        return RiesgoRepo(db).get_all()

    def get_all_by_revision(db: SqlDB, revision_id: int):
        return RiesgoRepo(db).get_all_by_revision(revision_id)

    def create(db: SqlDB, riesgo: RiesgoCreacion):
        return RiesgoRepo(db).create(riesgo)

    def update(db: SqlDB, id: int, riesgo: RiesgoActualizacion):
        return RiesgoRepo(db).update(id, riesgo)

    def get(db: SqlDB, id: int):
        riesgo = RiesgoRepo(db).get(id)

        if riesgo is None:
            raise HTTPException(status_code=404, detail="Riesgo no encontrado")

        return riesgo

    def buscar(db: SqlDB, revision_id: int, texto_buscado: str):
        return RiesgoRepo(db).buscar(revision_id, texto_buscado)

    # def delete(db: SqlDB, id: int):
    #     riesgo = RiesgoRepo(db).delete(id)

    #     if riesgo is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return riesgo
