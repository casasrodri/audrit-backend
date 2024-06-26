from database import BaseSchema
from sqlalchemy import Column, Date, Integer, String


class NormativaDB(BaseSchema):
    __tablename__ = "normativas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
