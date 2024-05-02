from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

relacion_riesgos_objetivos_control = Table(
    "relacion_riesgos_objetivos_control",
    Base.metadata,
    Column("riesgo_id", Integer, ForeignKey("riesgos.id"), primary_key=True),
    Column(
        "objetivo_control_id",
        Integer,
        ForeignKey("objetivos_control.id"),
        primary_key=True,
    ),
    extend_existing=True,
)
