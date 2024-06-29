from __future__ import annotations

from entidades.links.model import ElementoLinkeado
from entidades.revisiones.model import Revision
from models import BaseModel, FromAttributes


class ControlBase(BaseModel):
    nombre: str
    descripcion: str
    ejecutor: str
    oportunidad: str
    periodicidad: str
    automatizacion: str


class ControlResumido(BaseModel):
    id: int
    nombre: str
    descripcion: str


class ControlCreacion(ControlBase):
    revision_id: int


class ControlActualizacion(ControlCreacion): ...


class Control(ControlBase, FromAttributes):
    id: int
    revision: Revision
    links: list[ElementoLinkeado] = []


class ResultadoBusquedaControl(ControlBase):
    id: int
