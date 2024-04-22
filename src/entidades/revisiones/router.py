from fastapi import APIRouter
from .controller import RevisionesController
from .model import Revision, RevisionNodo, RevisionPorAuditoria

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=RevisionesController.get_all,
    methods=["GET"],
    response_model=list[Revision],
)

router.add_api_route(
    path="/auditoria/{auditoria_id}",
    endpoint=RevisionesController.get_all_auditoria,
    methods=["GET"],
    response_model=list[RevisionPorAuditoria],
)

router.add_api_route(
    path="/auditoria/{auditoria_id}/nodos",
    endpoint=RevisionesController.get_nodos,
    methods=["GET"],
    response_model=list[RevisionNodo],
)

router.add_api_route(
    path="/{id}",
    endpoint=RevisionesController.get,
    methods=["GET"],
    response_model=Revision,
)

router.add_api_route(
    path="",
    endpoint=RevisionesController.create,
    methods=["POST"],
    response_model=Revision,
    status_code=201,
)

router.add_api_route(
    path="/{id}",
    endpoint=RevisionesController.update,
    methods=["PUT"],
    response_model=Revision,
)

router.add_api_route(
    path="/{id}",
    endpoint=RevisionesController.delete,
    methods=["DELETE"],
    response_model=Revision,
)
