from datetime import datetime

from database import BaseSchema
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship


class ObservacionDB(BaseSchema):
    __tablename__ = "observaciones"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    riesgo = Column(String, index=True)
    responsable = Column(String, index=True)
    estado = Column(String, index=True)
    sector_auditoria = Column(String, index=True)
    efectos = Column(String, index=True)
    recomendaciones = Column(String, index=True)
    fecha_alta = Column(Date, index=True, default=datetime.now)
    fecha_solucion = Column(Date, index=True)

    # Relación uno-a-muchos con Revision
    revision_id = Column(Integer(), ForeignKey("revisiones.id"))
    revision = relationship("RevisionDB", back_populates="observaciones")

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} [{self.riesgo}] {self.nombre}>"
