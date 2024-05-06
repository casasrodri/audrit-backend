from __future__ import annotations
from models import BaseModel, FromAttributes
from typing import Any
from entidades.objetivos_control.model import ObjetivoControl
from entidades.revisiones.model import Revision


class RiesgoBase(BaseModel):
    nombre: str
    descripcion: str
    nivel: str


class RiesgoCreacion(RiesgoBase):
    objetivos_control: list[int]
    revision_id: int


class RiesgoActualizacion(RiesgoCreacion): ...


class Riesgo(RiesgoBase, FromAttributes):
    id: int
    revision: Revision
    objetivos_control: list[ObjetivoControl] = []
