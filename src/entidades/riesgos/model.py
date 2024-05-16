from __future__ import annotations
from models import BaseModel, FromAttributes
from entidades.objetivos_control.model import ObjetivoControl
from entidades.revisiones.model import Revision


class RiesgoBase(BaseModel):
    nombre: str
    descripcion: str
    nivel: str


class RiesgoResumido(RiesgoBase):
    id: int


class RiesgoCreacion(RiesgoBase):
    objetivos_control: list[int]
    revision_id: int


class RiesgoActualizacion(RiesgoCreacion): ...


# if TYPE_CHECKING:
from entidades.documentos.model import DocumentoDeRelevamiento
from entidades.controles.model import ControlResumido


class Riesgo(RiesgoBase, FromAttributes):
    id: int
    revision: Revision
    objetivos_control: list[ObjetivoControl] = []
    documentos: list[DocumentoDeRelevamiento] = []
    controles: list[ControlResumido] = []


class ResultadoBusquedaRiesgo(RiesgoBase):
    id: int
