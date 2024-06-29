from database import BaseSchema
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# from relaciones.tablas import controles_documentos, controles_riesgos


class ControlDB(BaseSchema):
    __tablename__ = "controles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
    # documentos = relationship(
    #     "DocumentoDB",
    #     secondary=controles_documentos,
    #     back_populates="controles",
    # )

    # Relación muchos-a-muchos con Riesgos
    # riesgos = relationship(
    #     "RiesgoDB",
    #     secondary=controles_riesgos,
    #     back_populates="controles",
    # )

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.nombre}>"
