from __future__ import annotations
from models import BaseModel, FromAttributes
from entidades.revisiones.model import Revision


class PruebaBase(BaseModel):
    nombre: str
    descripcion: str
    sector: str
    informe: str


class PruebaCreacion(PruebaBase):
    revision_id: int


class PruebaActualizacion(PruebaCreacion): ...


class Prueba(PruebaBase, FromAttributes):
    id: int
    revision: Revision


class ResultadoBusquedaPrueba(PruebaBase):
    id: int
