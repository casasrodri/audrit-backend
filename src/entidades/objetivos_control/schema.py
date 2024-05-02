from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import BaseSchema
from relaciones.tablas import relacion_riesgos_objetivos_control

from entidades.riesgos.schema import RiesgoSchema


class ObjetivoControlSchema(BaseSchema):
    __tablename__ = "objetivos_control"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)

    # Relación muchos-a-muchos con Riesgo
    riesgos = relationship(
        "RiesgoSchema",
        secondary=relacion_riesgos_objetivos_control,
        back_populates="objetivos_control",
    )

    def __repr__(self):
        return f"<ObjetivoControlDB {self.nombre}>"
