from __future__ import annotations
from enum import Enum
from models import BaseModel, FromAttributes
from entidades.links.model import ElementoLinkeado
from datetime import date
from pydantic import model_validator


class TipoNormativa(str, Enum):
    interna = "interna"
    externa = "externa"


class NormativaBase(BaseModel):
    nomenclatura: str
    nombre: str
    descripcion: str
    tipo: TipoNormativa
    emisor: str
    fecha_emision: date
    fecha_actualizacion: date
    comentarios: str | None = None


class NormativaResumida(BaseModel):
    id: int
    nombre: str
    descripcion: str


class NormativaCreacion(NormativaBase): ...


class NormativaActualizacion(NormativaCreacion): ...


class Normativa(NormativaBase, FromAttributes):
    id: int
    links: list[ElementoLinkeado] = []


class ResultadoBusquedaNormativa(NormativaBase):
    id: int

    @model_validator(mode="before")
    def completar_nombre(self):
        self.nombre = f"{self.nomenclatura} - {self.nombre}"
        return self
