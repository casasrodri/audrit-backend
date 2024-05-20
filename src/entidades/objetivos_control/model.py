from __future__ import annotations
from models import BaseModel, FromAttributes


class ObjetivoControlBase(BaseModel):
    nombre: str
    descripcion: str


class ObjetivoControlCreacion(ObjetivoControlBase): ...


# class RelevamientoActualizacion(RelevamientoCreacion): ...


class ObjetivoControl(ObjetivoControlBase, FromAttributes):
    id: int
