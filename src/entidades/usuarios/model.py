from pydantic import BaseModel


class UsuarioBase(BaseModel):
    email: str


class UsuarioLogin(UsuarioBase):
    password: str


class UsuarioOut(UsuarioBase):
    nombre: str
    apellido: str


class UsuarioDB(UsuarioOut, UsuarioLogin):
    pass
