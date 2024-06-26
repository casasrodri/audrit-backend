from database import BaseSchema
from middlewares.auth.schema import permisos
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship


class RolUsuarioDB(BaseSchema):
    __tablename__ = "roles_usuarios"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    menues = Column(String, index=True)
    endpoints = relationship("EndpointDB", secondary=permisos, back_populates="roles")

    usuarios = relationship(
        "UsuarioDB",
        back_populates="rol",
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.nombre}>"


class UsuarioDB(BaseSchema):
    __tablename__ = "usuarios"

    id = mapped_column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)

    # Relación uno-a-muchos con RolUsuarioDB
    rol_id = Column(Integer, ForeignKey("roles_usuarios.id"))
    rol = relationship("RolUsuarioDB", back_populates="usuarios")

    # Relación uno-a-muchos con PedidoDB
    pedidos_creados = relationship(
        "PedidoDB",
        foreign_keys="PedidoDB.creador_id",
        back_populates="creador",
    )
    pedidos_asignados = relationship(
        "PedidoDB",
        foreign_keys="PedidoDB.destinatario_id",
        back_populates="destinatario",
    )
    # Relación uno-a-muchos con ComentariosPedidosDB
    comentarios_pedidos = relationship(
        "ComentariosPedidosDB",
        back_populates="usuario",
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.nombre} {self.apellido}>"
