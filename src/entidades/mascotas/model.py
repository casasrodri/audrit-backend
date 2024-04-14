from models import BaseModel, FromAttributes


class MascotaBase(BaseModel):
    email: str


class MascotaCreacion(MascotaBase):
    password: str


class Mascota(MascotaBase, FromAttributes):
    id: int
    is_active: bool
