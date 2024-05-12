from __future__ import annotations
from models import BaseModel, FromAttributes
from entidades.revisiones.model import Revision


class ControlBase(BaseModel):
    nombre: str
    descripcion: str
    ejecutor: str
    oportunidad: str
    periodicidad: str
    automatizacion: str


class ControlCreacion(ControlBase):
    revision_id: int


class ControlActualizacion(ControlCreacion): ...


# if TYPE_CHECKING:
from entidades.documentos.model import DocumentoDeRelevamiento


class Control(ControlBase, FromAttributes):
    id: int
    revision: Revision
    documentos: list[DocumentoDeRelevamiento] = []


class ResultadoBusquedaControl(ControlBase):
    id: int
