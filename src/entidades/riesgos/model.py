from __future__ import annotations
from models import BaseModel, FromAttributes
from entidades.objetivos_control.model import ObjetivoControl
from entidades.revisiones.model import Revision
from pydantic import PydanticUndefinedAnnotation


class RiesgoBase(BaseModel):
    nombre: str
    descripcion: str
    nivel: str


class RiesgoCreacion(RiesgoBase):
    objetivos_control: list[int]
    revision_id: int


class RiesgoActualizacion(RiesgoCreacion): ...


# if TYPE_CHECKING:
from entidades.documentos.model import DocumentoDeRelevamiento


class Riesgo(RiesgoBase, FromAttributes):
    id: int
    revision: Revision
    objetivos_control: list[ObjetivoControl] = []
    documentos: list[DocumentoDeRelevamiento] = []


class ResultadoBusquedaRiesgo(RiesgoBase):
    id: int
