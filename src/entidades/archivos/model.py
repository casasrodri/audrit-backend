from __future__ import annotations
from models import BaseModel, FromAttributes
from entidades.revisiones.model import Revision
from entidades.links.model import ElementoLinkeado
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
