from database import BaseSchema
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ArchivoDB(BaseSchema):
    __tablename__ = "archivos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    bytes = Column(Integer, index=True)
    tipo = Column(String, index=True)
    path = Column(String, index=True)

    pedido_id = Column(Integer(), ForeignKey("pedidos.id"))
    pedido = relationship("PedidoDB", back_populates="archivos")

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} [{self.tipo}] {self.nombre}>"
