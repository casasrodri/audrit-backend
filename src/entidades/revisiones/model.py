from __future__ import annotations

from models import BaseModel, FromAttributes

from entidades.auditorias.model import Auditoria


class RevisionBase(BaseModel):
    sigla: str
    nombre: str
    descripcion: str
    estado: str
    informe: str | None


class RevisionCreacion(RevisionBase):
    padre_id: int | None


class RevisionActualizacion(RevisionCreacion): ...


class Revision(RevisionBase, FromAttributes):
    id: int
    auditoria: Auditoria
    padre: Revision | None


class RevisionPorAuditoria(RevisionBase, FromAttributes):
    id: int
    padre: RevisionPorAuditoria | None


class RevisionNodoData(BaseModel):
    id: int
    sigla: str
    nombre: str
    descripcion: str
    estado: str
    informe: str | None
    padre: int | None


class RevisionNodo(BaseModel):
    key: int
    label: str
    data: RevisionNodoData
    children: list[RevisionNodo] = []
