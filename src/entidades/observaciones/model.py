from __future__ import annotations

from datetime import date, datetime

from models import BaseModel, FromAttributes

from entidades.links.model import ElementoLinkeado
from entidades.revisiones.model import Revision


class ObservacionBase(BaseModel):
    nombre: str
    descripcion: str
    riesgo: str
    responsable: str
    estado: str
    sector_auditoria: str
    efectos: str
    recomendaciones: str
    fecha_alta: date | None = datetime.now().date()
    fecha_solucion: date | None


class ObservacionResumida(ObservacionBase):
    id: int


class ObservacionCreacion(ObservacionBase):
    revision_id: int


class ObservacionActualizacion(ObservacionCreacion): ...


class Observacion(ObservacionBase, FromAttributes):
    id: int
    revision: Revision
    links: list[ElementoLinkeado] = []


class ResultadoBusquedaObservacion(BaseModel):
    id: int
    nombre: str
    descripcion: str
    riesgo: str
    efectos: str
    recomendaciones: str
