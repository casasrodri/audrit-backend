from database import BaseSchema
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class PruebaDB(BaseSchema):
    __tablename__ = "pruebas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    sector = Column(String, index=True)
    informe = Column(String, index=True)

    # Relación uno-a-muchos con Revision
    revision_id = Column(Integer(), ForeignKey("revisiones.id"))
    revision = relationship("RevisionDB", back_populates="pruebas")

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} {self.nombre}>"
