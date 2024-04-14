from __future__ import annotations
from models import BaseModel, FromAttributes
from typing import Any


class CicloBase(BaseModel):
    nombre: str
    sigla: str
    descripcion: str


class CicloCreacion(CicloBase):
    padre_id: int | None


class CicloActualizacion(CicloCreacion): ...


class Ciclo(CicloBase, FromAttributes):
    id: int
    padre: Ciclo | None


class CicloNodoData(BaseModel):
    id: int
    nombre: str
    sigla: str
    descripcion: str
    padre: int | None


class CicloNodo(BaseModel):
    key: int
    label: str
    data: CicloNodoData
    children: list[CicloNodo] = []
