from datetime import datetime

from database import BaseSchema
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ComentariosPedidosDB(BaseSchema):
    __tablename__ = "comentarios_pedidos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    momento = Column(DateTime, index=True, default=datetime.now)

    pedido_id = Column(Integer(), ForeignKey("pedidos.id"))
    pedido = relationship("PedidoDB", back_populates="comentarios")

    usuario_id = Column(Integer(), ForeignKey("usuarios.id"))
    usuario = relationship("UsuarioDB", back_populates="comentarios_pedidos")

    texto = Column(String, index=True)


class PedidoDB(BaseSchema):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    estado = Column(String, index=True)
    fecha_vencimiento = Column(Date, index=True)

    creador_id = Column(Integer(), ForeignKey("usuarios.id"))
    creador = relationship(
        "UsuarioDB", back_populates="pedidos_creados", foreign_keys=[creador_id]
    )

    destinatario_id = Column(Integer(), ForeignKey("usuarios.id"))
    destinatario = relationship(
        "UsuarioDB", back_populates="pedidos_asignados", foreign_keys=[destinatario_id]
    )

    comentarios = relationship("ComentariosPedidosDB", back_populates="pedido")
    archivos = relationship("ArchivoDB", back_populates="pedido")

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} [{self.estado}] {self.nombre}>"
