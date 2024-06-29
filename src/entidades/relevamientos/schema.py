from database import BaseSchema
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class RelevamientoDB(BaseSchema):
    __tablename__ = "relevamientos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
        return f"<{self.__class__.__name__}:{self.id} {self.nombre}>"
