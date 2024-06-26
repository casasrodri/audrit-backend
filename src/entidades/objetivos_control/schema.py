from database import BaseSchema
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column


class ObjetivoControlDB(BaseSchema):
    __tablename__ = "objetivos_control"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.nombre}>"
