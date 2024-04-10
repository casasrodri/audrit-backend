from .base import BaseModel, FromAttributes


class AuditoriaBase(BaseModel):
    sigla: str
    nombre: str
    tipo: str
    estado: str
    periodo: str


class Auditoria(AuditoriaBase, FromAttributes):
    id: int


class AuditoriaCreacion(AuditoriaBase): ...
