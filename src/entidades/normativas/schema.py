from sqlalchemy import Column, Integer, String, Date
from database import BaseSchema


class NormativaDB(BaseSchema):
    __tablename__ = "normativas"

    id = Column(Integer, primary_key=True, index=True)
    nomenclatura = Column(String, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    tipo = Column(String, index=True)
    emisor = Column(String, index=True)
    fecha_emision = Column(Date, index=True)
    fecha_actualizacion = Column(Date, index=True)
    comentarios = Column(String, index=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.nombre}>"
