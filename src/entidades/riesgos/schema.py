from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import BaseSchema
from sqlalchemy.orm import mapped_column
from relaciones.tablas import riesgos_objetivos_control


class RiesgoSchema(BaseSchema):
    __tablename__ = "riesgos"

    id = mapped_column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    nivel = Column(String, index=True)

    # Relación muchos-a-muchos con ObjetivoControl
    objetivos_control = relationship(
        "ObjetivoControlSchema",
        secondary=lambda: riesgos_objetivos_control,
        back_populates="riesgos",
    )

    # Relación uno-a-muchos con Revision
    revision_id = Column(Integer(), ForeignKey("revisiones.id"))
    revision = relationship("RevisionSchema", back_populates="riesgos")

    def __repr__(self):
        return f"<RiesgoDB {self.nombre}>"
