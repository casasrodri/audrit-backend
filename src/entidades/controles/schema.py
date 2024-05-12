from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import BaseSchema

# from sqlalchemy.orm import mapped_column
from relaciones.tablas import controles_documentos


class ControlDB(BaseSchema):
    __tablename__ = "controles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    ejecutor = Column(String, index=True)
    oportunidad = Column(String, index=True)
    periodicidad = Column(String, index=True)
    automatizacion = Column(String, index=True)

    # Relación uno-a-muchos con Revision
    revision_id = Column(Integer(), ForeignKey("revisiones.id"))
    revision = relationship("RevisionDB", back_populates="controles")

    # Relación muchos-a-muchos con Documentos
    documentos = relationship(
        "DocumentoDB",
        secondary=controles_documentos,
        back_populates="controles",
    )

    def __repr__(self):
        return f"<ControlDB:{self.id} {self.nombre}>"
