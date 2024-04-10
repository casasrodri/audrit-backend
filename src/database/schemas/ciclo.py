from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.base import BaseSchema


class CicloSchema(BaseSchema):
    __tablename__ = "ciclos"

    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

    padre_id = Column(Integer, ForeignKey("ciclos.id"))
    padre = relationship("CicloSchema", remote_side=[id])

    def __repr__(self):
        return f"<CicloDB {self.nombre}>"
