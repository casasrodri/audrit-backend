from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import BaseSchema
from entidades.revisiones.schema import RevisionSchema


class RelevamientoSchema(BaseSchema):
    __tablename__ = "relevamientos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, index=True)

    revision_id = Column(Integer, ForeignKey("revisiones.id"))
    revision = relationship(
        "RevisionSchema",
        back_populates="relevamientos",
        remote_side="RevisionSchema.id",
    )

    sigla = Column(String, index=True)
    nombre = Column(String, index=True)

    padre_id = Column(Integer, ForeignKey("relevamientos.id"))
    padre = relationship("RelevamientoSchema", remote_side=[id])

    documentos = relationship(
        "DocumentoSchema",
        back_populates="relevamiento",
        foreign_keys="DocumentoSchema.relevamiento_id",
    )

    def __repr__(self):
        return f"<RelevamientoDB {self.nombre}>"
