from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import BaseSchema
from sqlalchemy.orm import mapped_column
from relaciones.tablas import riesgos_objetivos_control, riesgos_documentos


class RiesgoDB(BaseSchema):
    __tablename__ = "riesgos"

    id = mapped_column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    nivel = Column(String, index=True)

    # Relación uno-a-muchos con Revision
    revision_id = Column(Integer(), ForeignKey("revisiones.id"))
    revision = relationship("RevisionDB", back_populates="riesgos")

    # Relación muchos-a-muchos con ObjetivoControl
    objetivos_control = relationship(
        "ObjetivoControlDB",
        secondary=riesgos_objetivos_control,
        back_populates="riesgos",
    )

    # Relación muchos-a-muchos con Documentos
    documentos = relationship(
        "DocumentoDB",
        secondary=riesgos_documentos,
        back_populates="riesgos",
    )

    def __repr__(self):
        return f"<RiesgoDB:{self.id} {self.nombre}>"
