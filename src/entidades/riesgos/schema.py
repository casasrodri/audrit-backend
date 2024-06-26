from database import BaseSchema
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

# from relaciones.tablas import (
#     riesgos_objetivos_control,
#     riesgos_documentos,
#     controles_riesgos,
# )


class RiesgoDB(BaseSchema):
    __tablename__ = "riesgos"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    nivel = Column(String, index=True)

    # Relación uno-a-muchos con Revision
    revision_id = Column(Integer(), ForeignKey("revisiones.id"))
    revision = relationship("RevisionDB", back_populates="riesgos")

    # Relación muchos-a-muchos con ObjetivoControl
    # objetivos_control = relationship(
    #     "ObjetivoControlDB",
    #     secondary=riesgos_objetivos_control,
    #     back_populates="riesgos",
    # )

    # Relación muchos-a-muchos con Documentos
    # documentos = relationship(
    #     "DocumentoDB",
    #     secondary=riesgos_documentos,
    #     back_populates="riesgos",
    # )

    # Relación muchos-a-muchos con Controles
    # controles = relationship(
    #     "ControlDB",
    #     secondary=controles_riesgos,
    #     back_populates="riesgos",
    # )

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.nombre}>"
