from sqlalchemy import Column, Integer, String
from database import BaseSchema


class AuditoriaDB(BaseSchema):
    __tablename__ = "auditorias"

    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String, index=True, unique=True)
    nombre = Column(String, index=True)
    # TODO: Relacionar con una tabla "AuditoriasTipos"
    tipo = Column(String, index=True)
    # TODO: Relacionar con una tabla "AuditoriasEstados"
    estado = Column(String, index=True)
    periodo = Column(String, index=True)

    def __repr__(self):
        return f"<AuditoriaDB:{self.id} {self.nombre}>"
