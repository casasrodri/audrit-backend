from __future__ import annotations

from entidades.links.model import ElementoLinkeado
from entidades.revisiones.model import Revision
from models import BaseModel, FromAttributes


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
    links: list[ElementoLinkeado] = []


class ResultadoBusquedaPrueba(PruebaBase):
    id: int
