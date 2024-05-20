from sqlalchemy import Column, Integer, String
from database import BaseSchema


class LinkDB(BaseSchema):
    __tablename__ = "links"

    id = Column(String, primary_key=True)
    ent1 = Column(String, nullable=False)
    id1 = Column(Integer, nullable=False)
    ent2 = Column(String, nullable=False)
    id2 = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<LinkDB:{self.id}>"
