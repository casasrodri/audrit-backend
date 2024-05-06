from sqlalchemy import Column, ForeignKey, Integer, Table
from database import BaseSchema

riesgos_objetivos_control = Table(
    "riesgos_objctrl",
    BaseSchema.metadata,
    Column("riesgo_id", Integer, ForeignKey("riesgos.id"), primary_key=True),
    Column(
        "objetivo_control_id",
        Integer,
        ForeignKey("objetivos_control.id"),
        primary_key=True,
    ),
    extend_existing=True,
)
