from enum import Enum

from models import BaseModel, FromAttributes


class EntidadLinkeable(str, Enum):
    aplicacion = "aplicacion"
    control = "control"
    normativa = "normativa"
    objetivo_control = "objetivo_control"
    organigrama = "organigrama"
    prueba = "prueba"
    relevamiento = "relevamiento"
    riesgo = "riesgo"
    observacion = "observacion"


class ElementoLinkeado(BaseModel, FromAttributes):
    id: int
    nombre: str
    entidad: EntidadLinkeable
