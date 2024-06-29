from __future__ import annotations

from entidades.links.model import ElementoLinkeado
from models import BaseModel, FromAttributes


class AplicacionBase(BaseModel):
    nombre: str
    descripcion: str
    desarrollador: str | None = None
    version: str | None = None
    referentes: str | None = None
    comentarios: str | None = None


class AplicacionResumida(BaseModel):
    id: int
    nombre: str
    descripcion: str


class AplicacionCreacion(AplicacionBase): ...


class AplicacionActualizacion(AplicacionCreacion): ...


class Aplicacion(AplicacionBase, FromAttributes):
    id: int
    links: list[ElementoLinkeado] = []


class ResultadoBusquedaAplicacion(AplicacionBase):
    id: int
