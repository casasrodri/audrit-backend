from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import BaseSchema


class RevisionDB(BaseSchema):
    __tablename__ = "revisiones"

    id = Column(Integer, primary_key=True, index=True)
    auditoria_id = Column(
        Integer,
        ForeignKey("auditorias.id"),
    )
    auditoria = relationship("AuditoriaDB", remote_side="AuditoriaDB.id")

    sigla = Column(String, index=True, nullable=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)

    padre_id = Column(Integer, ForeignKey("revisiones.id"), nullable=True)
    padre = relationship("RevisionDB", remote_side="RevisionDB.id")

    estado = Column(String, index=True)
    informe = Column(String)

    relevamientos = relationship("RelevamientoDB", back_populates="revision")
    riesgos = relationship(
        "RiesgoDB",
        back_populates="revision",
    )
    controles = relationship(
        "ControlDB",
        back_populates="revision",
    )
    pruebas = relationship(
        "PruebaDB",
        back_populates="revision",
    )

    def __repr__(self):
        return f"<RevisionDB:{self.id} {self.nombre}>"
