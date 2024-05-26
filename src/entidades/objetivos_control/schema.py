from sqlalchemy import Column, Integer, String
from database import BaseSchema
from sqlalchemy.orm import mapped_column

# from relaciones.tablas import riesgos_objetivos_control

from entidades.riesgos.schema import RiesgoDB


class ObjetivoControlDB(BaseSchema):
    __tablename__ = "objetivos_control"

    id = mapped_column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)

    # Relación muchos-a-muchos con Riesgo
    # riesgos = relationship(
    #     "RiesgoDB",
    #     secondary=riesgos_objetivos_control,
    #     back_populates="objetivos_control",
    # )

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.nombre}>"
