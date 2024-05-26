from pydantic import BaseModel
from enum import Enum


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


class UsuarioOut(UsuarioBase):
    class Rol(BaseModel):
        nombre: str
        descripcion: str

    id: int
    rol: Rol


class UsuarioAutenticacion(UsuarioOut, UsuarioLogin):
    pass
