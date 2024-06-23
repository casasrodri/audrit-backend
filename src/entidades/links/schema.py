from sqlalchemy import Column, Integer, String
from database import BaseSchema


class LinkDB(BaseSchema):
    __tablename__ = "links"

    id = Column(String, primary_key=True, autoincrement=True)
    ent1 = Column(String, nullable=False)
    id1 = Column(Integer, nullable=False)
    ent2 = Column(String, nullable=False)
    id2 = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.id}>"


# archivos_pedidos = Table(
#     "archivos_pedidos",
#     BaseSchema.metadata,
#     Column(
#         "pedido_id", Integer, ForeignKey("pedidos.id"), primary_key=True
#     ),
#     Column(
#         "archivo_id",
#         Integer,
#         ForeignKey("archivos.id"),
#         primary_key=True,
#     ),
#     extend_existing=True,
# )
