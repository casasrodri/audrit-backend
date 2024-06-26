from __future__ import annotations

from datetime import date, datetime

from models import BaseModel, FromAttributes

from entidades.archivos.model import ArchivoResumido
from entidades.usuarios.model import UsuarioOut


class PedidoBase(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    fecha_vencimiento: date | None


class PedidoMin(PedidoBase):
    id: int
    nombre: str
    descripcion: str


# class PedidoResumida(PedidoBase):
#     id: int


class PedidoCreacion(PedidoBase):
    creador_id: int
    destinatario_id: int


class PedidoActualizacion(PedidoBase):
    destinatario_id: int


class ComentarioPedidoCreacion(BaseModel):
    usuario_id: int
    texto: str


class ComentarioPedido(BaseModel):
    id: int
    momento: datetime
    pedido: PedidoMin
    usuario: UsuarioOut
    texto: str


class Pedido(PedidoBase, FromAttributes):
    id: int
    creador: UsuarioOut
    destinatario: UsuarioOut
    comentarios: list[ComentarioPedido] = []
    archivos: list[ArchivoResumido] = []


# class ResultadoBusquedaPedido(BaseModel):
#     id: int
#     nombre: str
#     descripcion: str
#     riesgo: str
#     efectos: str
#     recomendaciones: str
