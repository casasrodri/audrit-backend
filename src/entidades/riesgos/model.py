from __future__ import annotations

from models import BaseModel, FromAttributes

from entidades.links.model import ElementoLinkeado
from entidades.revisiones.model import Revision


class RiesgoBase(BaseModel):
    nombre: str
    descripcion: str
    nivel: str


class RiesgoResumido(RiesgoBase):
    id: int


class RiesgoCreacion(RiesgoBase):
    objetivos_control: list[int]
    revision_id: int


class RiesgoActualizacion(RiesgoCreacion): ...


class Riesgo(RiesgoBase, FromAttributes):
    id: int
    revision: Revision
    links: list[ElementoLinkeado] = []


class ResultadoBusquedaRiesgo(RiesgoBase):
    id: int
