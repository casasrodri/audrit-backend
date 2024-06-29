from fastapi import APIRouter
from models import ResultadoBusquedaGlobal

from .controller import AuditoriasController
from .model import Auditoria

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=AuditoriasController.get_all,
    methods=["GET"],
    response_model=list[Auditoria],
)

router.add_api_route(
    path="",
    endpoint=AuditoriasController.create,
    methods=["POST"],
    response_model=Auditoria,
    status_code=201,
)

router.add_api_route(
    path="/sigla/{sigla}",
    endpoint=AuditoriasController.get_by_sigla,
    methods=["GET"],
    response_model=Auditoria,
)

router.add_api_route(
    path="/{id}",
    endpoint=AuditoriasController.get_by_id,
    methods=["GET"],
    response_model=Auditoria,
)

router.add_api_route(
    path="/{id}",
    endpoint=AuditoriasController.update,
    methods=["PUT"],
    response_model=Auditoria,
)

router.add_api_route(
    path="/buscarGlobal/{texto:path}",
    endpoint=AuditoriasController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
