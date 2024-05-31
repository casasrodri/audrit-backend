from __future__ import annotations
from models import BaseModel, FromAttributes
from entidades.links.model import ElementoLinkeado
from datetime import date


class AplicacionBase(BaseModel):
    nombre: str
    descripcion: str
    desarrollador: str
    version: str
    referentes: str
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
