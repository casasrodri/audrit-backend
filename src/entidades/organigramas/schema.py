from database import BaseSchema
from sqlalchemy import Column, Integer, String


class OrganigramaDB(BaseSchema):
    __tablename__ = "organigramas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    gerencia = Column(String, index=True)
    personas = Column(String, index=True)
    comentarios = Column(String, index=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.nombre}>"
