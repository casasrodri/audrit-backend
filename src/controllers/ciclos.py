from .base import BaseController
from fastapi import HTTPException
from database.base import SqlDB
from repositories.ciclos import CiclosRepo
from models.ciclos import CicloCreacion, CicloNodo, CicloNodoData


class CiclosController(BaseController):
    def get_all(db: SqlDB):
        return CiclosRepo(db).get_all()

    def get_nodos(db: SqlDB):
        ciclos = CiclosRepo(db).get_all()

        def crear_nodo(ciclo):
            data = CicloNodoData(
                id=ciclo.id,
                nombre=ciclo.nombre,
                sigla=ciclo.sigla,
                sigla_extendida=ciclo.sigla_extendida,
                descripcion=ciclo.descripcion,
                padre=ciclo.padre_id,
            )

            return CicloNodo(
                key=ciclo.id,
                label=ciclo.nombre,
                data=data,
                children=[],
            )

        nodos = {ciclo.id: crear_nodo(ciclo) for ciclo in ciclos}

        for nodo in nodos.copy().values():
            if nodo.data.padre:
                id_padre = nodo.data.padre
                nodos[id_padre].children.append(nodo)

        out = [nodo for nodo in nodos.values() if nodo.data.padre is None]
        return out

    def create(db: SqlDB, ciclo: CicloCreacion):
        return CiclosRepo(db).create(ciclo)
