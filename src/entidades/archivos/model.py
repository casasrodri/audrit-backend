from __future__ import annotations

from entidades.links.model import ElementoLinkeado
from entidades.revisiones.model import Revision
from models import BaseModel, FromAttributes
from pydantic import model_validator


class ArchivoBase(BaseModel):
    nombre: str
    bytes: int
    tipo: str


class ArchivoResumido(ArchivoBase):
    id: int
    link: str

    @model_validator(mode="before")
    def add_link(self):
        self.link = self.path.split("/")[-1]
        return self


class Archivo(ArchivoBase, FromAttributes):
    id: int
    pedidos: Revision
    pedidos: list[ElementoLinkeado] = []


class ResultadoBusquedaArchivo(BaseModel):
    id: int
    nombre: str
