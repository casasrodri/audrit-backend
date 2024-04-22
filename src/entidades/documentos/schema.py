from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import BaseSchema
from entidades.relevamientos.schema import RelevamientoSchema


class DocumentoSchema(BaseSchema):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)

    relevamiento_id = Column(Integer, ForeignKey("relevamientos.id"))
    relevamiento = relationship(
        "RelevamientoSchema",
        back_populates="documentos",
        foreign_keys=[relevamiento_id],
        # remote_side="RelevamientoSchema.id",
    )
    contenido = Column(String, index=True)

    def __repr__(self):
        return f"<DocumentoDB {self.relevamiento.nombre}>"
