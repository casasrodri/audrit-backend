from enum import Enum

from models import FromAttributes
from pydantic import BaseModel, model_validator

# from middlewares.auth.model import Endpoint


class RolUsuario(str, Enum):
    AuditorAnalista = "Auditor Analista"
    AuditorSupervisor = "Auditor Supervisor"
    Auditado = "Auditado"
    Inspector = "Inspector"


class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: str


class UsuarioCreacion(UsuarioBase):
    password: str
    rol_nombre: RolUsuario


class UsuarioLogin(BaseModel):
    email: str
    password: str


class UsuarioOut(FromAttributes, UsuarioBase):
    class Rol(BaseModel):
        nombre: str
        descripcion: str
        # endpoints: list[Endpoint]

    id: int
    nombre: str
    apellido: str
    nombre_completo: str
    rol: Rol

    @model_validator(mode="before")
    def add_nombre_completo(self):
        self.nombre_completo = f"{self.nombre} {self.apellido}"
        return self


class UsuarioAutenticacion(UsuarioOut, UsuarioLogin):
    pass
