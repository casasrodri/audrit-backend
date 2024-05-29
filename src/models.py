from pydantic import BaseModel
from typing import Any


class FromAttributes:
    "Permite que los modelos se inicialicen con los atributos que se le pasen al constructor."

    class Config:
        from_attributes = True
        # extra = "forbid"


class ResultadoBusquedaGlobal(FromAttributes, BaseModel):
    nombre: str
    texto: str | None
    tipo: str
    objeto: dict

    def __hash__(self) -> int:
        return hash(self.nombre + self.texto + self.tipo)

    def __repr__(self) -> str:
        return f"< ResultadoBusquedaGlobal[{self.tipo}] {self.nombre} | {self.texto} >"
