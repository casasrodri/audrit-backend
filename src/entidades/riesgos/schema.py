from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import BaseSchema
from relaciones.tablas import relacion_riesgos_objetivos_control


class RiesgoSchema(BaseSchema):
    __tablename__ = "riesgos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    nivel = Column(String, index=True)

    # Relación uno-a-muchos con ObjetivoControl
    objetivos_control = relationship(
        "ObjetivoControlSchema",
        secondary=relacion_riesgos_objetivos_control,
        back_populates="riesgos",
    )

    def __repr__(self):
        return f"<RiesgoDB {self.nombre}>"
