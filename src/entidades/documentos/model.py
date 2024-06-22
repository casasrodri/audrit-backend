from __future__ import annotations
from models import BaseModel, FromAttributes
from entidades.relevamientos.model import Relevamiento, RelevamientoId
from datetime import datetime


class DocumentoBase(BaseModel):
    contenido: str | None


class DocumentoCreacion(DocumentoBase):
    relevamiento_id: int


class DocumentoActualizacion(DocumentoCreacion): ...


class DocumentoSoloContenido(DocumentoBase):
    id: int


class DocumentoDeRelevamiento(BaseModel):
    id: int
    actualizacion: datetime
    relevamiento: RelevamientoId


# from entidades.riesgos.model import ResultadoBusquedaRiesgo


class Documento(DocumentoBase, FromAttributes):
    id: int
    relevamiento: Relevamiento
    # riesgos: list[ResultadoBusquedaRiesgo] = []
