from sqlalchemy import Column, Integer, String
from database import BaseSchema


class AplicacionDB(BaseSchema):
    __tablename__ = "aplicaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    desarrollador = Column(String, index=True)
    version = Column(String, index=True)
    referentes = Column(String, index=True)
    comentarios = Column(String, index=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.nombre}>"
