from __future__ import annotations
from models import BaseModel, FromAttributes
from typing import Any
from entidades.revisiones.model import Revision


class RelevamientoBase(BaseModel):
    tipo: str
    sigla: str | None
    nombre: str


class RelevamientoCreacion(RelevamientoBase):
    revision_id: int
    padre_id: int | None


class RelevamientoActualizacion(RelevamientoCreacion): ...


class Relevamiento(RelevamientoBase, FromAttributes):
    id: int
    revision: Revision
    padre: Relevamiento | None


class RelevamientoNodoData(RelevamientoBase):
    # TODO Corregir
    id: int
    revision: int
    padre: int | None


class RelevamientoNodo(BaseModel):
    key: int
    label: str
    data: RelevamientoNodoData
    children: list[RelevamientoNodo] = []