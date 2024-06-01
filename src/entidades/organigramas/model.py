from __future__ import annotations
from models import BaseModel, FromAttributes
from entidades.links.model import ElementoLinkeado
from datetime import date


class OrganigramaBase(BaseModel):
    nombre: str
    descripcion: str
    gerencia: str
    personas: str | None = None
    comentarios: str | None = None


class OrganigramaResumido(BaseModel):
    id: int
    nombre: str
    descripcion: str


class OrganigramaCreacion(OrganigramaBase): ...


class OrganigramaActualizacion(OrganigramaCreacion): ...


class Organigrama(OrganigramaBase, FromAttributes):
    id: int
    links: list[ElementoLinkeado] = []


class ResultadoBusquedaOrganigrama(OrganigramaBase):
    id: int
