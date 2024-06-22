from __future__ import annotations
from models import BaseModel, FromAttributes
from entidades.revisiones.model import Revision
from entidades.links.model import ElementoLinkeado


class RelevamientoBase(BaseModel):
    tipo: str
    sigla: str | None
    nombre: str


class RelevamientoCreacion(RelevamientoBase):
    revision_id: int
    padre_id: int | None


class RelevamientoActualizacion(RelevamientoCreacion): ...


class RelevamientoId(BaseModel):
    id: int
    nombre: str


# from entidades.documentos.model import Documento


class Relevamiento(RelevamientoBase, FromAttributes):
    id: int
    revision: Revision
    padre: Relevamiento | None
    links: list[ElementoLinkeado] = []


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
