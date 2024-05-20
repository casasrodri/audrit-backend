from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import BaseSchema


class RelevamientoDB(BaseSchema):
    __tablename__ = "relevamientos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, index=True)

    revision_id = Column(Integer, ForeignKey("revisiones.id"))
    revision = relationship(
        "RevisionDB",
        back_populates="relevamientos",
        remote_side="RevisionDB.id",
    )

    sigla = Column(String, index=True)
    nombre = Column(String, index=True)

    padre_id = Column(Integer, ForeignKey("relevamientos.id"))
    padre = relationship("RelevamientoDB", remote_side=[id])

    documentos = relationship(
        "DocumentoDB",
        back_populates="relevamiento",
        foreign_keys="DocumentoDB.relevamiento_id",
    )

    def __repr__(self):
        return f"<RelevamientoDB:{self.id} {self.nombre}>"
