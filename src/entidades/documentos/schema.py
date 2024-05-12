from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import BaseSchema
from entidades.relevamientos.schema import RelevamientoDB
from relaciones.tablas import riesgos_documentos, controles_documentos


class DocumentoDB(BaseSchema):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)

    relevamiento_id = Column(Integer, ForeignKey("relevamientos.id"))
    relevamiento = relationship(
        "RelevamientoDB",
        back_populates="documentos",
        foreign_keys=[relevamiento_id],
        # remote_side="RelevamientoDB.id",
    )

    contenido = Column(String, index=True)

    # Relación muchos-a-muchos con Riesgo
    riesgos = relationship(
        "RiesgoDB",
        secondary=riesgos_documentos,
        back_populates="documentos",
    )
    controles = relationship(
        "ControlDB",
        secondary=controles_documentos,
        back_populates="documentos",
    )

    def __repr__(self):
        return f"<DocumentoDB:{self.id} {self.relevamiento.nombre}>"
