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

riesgos_documentos = Table(
    "riesgos_documentos",
    BaseSchema.metadata,
    Column("riesgo_id", Integer, ForeignKey("riesgos.id"), primary_key=True),
    Column(
        "documento_id",
        Integer,
        ForeignKey("documentos.id"),
        primary_key=True,
    ),
    extend_existing=True,
)


controles_documentos = Table(
    "controles_documentos",
    BaseSchema.metadata,
    Column("control_id", Integer, ForeignKey("controles.id"), primary_key=True),
    Column(
        "documento_id",
        Integer,
        ForeignKey("documentos.id"),
        primary_key=True,
    ),
    extend_existing=True,
)

controles_riesgos = Table(
    "controles_riesgos",
    BaseSchema.metadata,
    Column("control_id", Integer, ForeignKey("controles.id"), primary_key=True),
    Column(
        "riesgo_id",
        Integer,
        ForeignKey("riesgos.id"),
        primary_key=True,
    ),
    extend_existing=True,
)
