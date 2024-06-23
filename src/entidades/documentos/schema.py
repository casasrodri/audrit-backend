from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import BaseSchema


class DocumentoDB(BaseSchema):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contenido = Column(String)
    actualizacion = Column(DateTime, index=True)

    relevamiento_id = Column(Integer, ForeignKey("relevamientos.id"))
    relevamiento = relationship(
        "RelevamientoDB",
        back_populates="documentos",
        foreign_keys=[relevamiento_id],
        # remote_side="RelevamientoDB.id",
    )

    # Relación muchos-a-muchos con Riesgo
    # riesgos = relationship(
    #     "RiesgoDB",
    #     secondary=riesgos_documentos,
    #     back_populates="documentos",
    # )
    # controles = relationship(
    #     "ControlDB",
    #     secondary=controles_documentos,
    #     back_populates="documentos",
    # )

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.relevamiento.nombre}>"
