from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import BaseSchema

permisos = Table(
    "permisos",
    BaseSchema.metadata,
    Column("endpoint_id", Integer, ForeignKey("endpoints.id"), primary_key=True),
    Column("rol_id", Integer, ForeignKey("roles_usuarios.id"), primary_key=True),
)


class EndpointDB(BaseSchema):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, index=True)
    path = Column(String, index=True)

    roles = relationship("RolUsuarioDB", secondary=permisos, back_populates="endpoints")

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id} [{self.method}] {self.path}>"

    def __eq__(self, other):
        return self.method == other.method and self.path == other.path
