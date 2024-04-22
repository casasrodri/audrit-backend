from __future__ import annotations
from models import BaseModel, FromAttributes
from typing import Any
from entidades.relevamientos.model import Relevamiento


class DocumentoBase(BaseModel):
    contenido: str | None


class DocumentoCreacion(DocumentoBase):
    relevamiento_id: int


class DocumentoActualizacion(DocumentoCreacion): ...


class DocumentoSoloContenido(DocumentoBase):
    id: int


class Documento(DocumentoBase, FromAttributes):
    id: int
    relevamiento: Relevamiento
