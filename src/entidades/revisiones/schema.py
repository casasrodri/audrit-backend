from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import BaseSchema


class RevisionSchema(BaseSchema):
    __tablename__ = "revisiones"

    id = Column(Integer, primary_key=True, index=True)
    auditoria_id = Column(
        Integer,
        ForeignKey("auditorias.id"),
    )
    auditoria = relationship("AuditoriaSchema", remote_side="AuditoriaSchema.id")

    sigla = Column(String, index=True, nullable=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)

    padre_id = Column(Integer, ForeignKey("revisiones.id"), nullable=True)
    padre = relationship("RevisionSchema", remote_side="RevisionSchema.id")

    estado = Column(String, index=True)
    informe = Column(String)

    relevamientos = relationship("RelevamientoSchema", back_populates="revision")
    riesgos = relationship(
        "RiesgoSchema",
        back_populates="revision",
    )

    def __repr__(self):
        return f"<RevisionDB {self.nombre}>"
