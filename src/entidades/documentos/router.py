from fastapi import APIRouter
from .controller import DocumentosController
from .model import Documento, DocumentoSoloContenido

router = APIRouter()

# OK
router.add_api_route(
    path="",
    endpoint=DocumentosController.get_all,
    methods=["GET"],
    response_model=list[Documento],
)

# OK
router.add_api_route(
    path="/{id}",
    endpoint=DocumentosController.get,
    methods=["GET"],
    response_model=Documento,
)

# OK
router.add_api_route(
    path="/relevamiento/{relevamiento_id}",
    endpoint=DocumentosController.get_by_relevamiento,
    methods=["GET"],
    response_model=DocumentoSoloContenido,
)

# OK
router.add_api_route(
    path="",
    endpoint=DocumentosController.create,
    methods=["POST"],
    response_model=Documento,
    status_code=201,
)

# TODO
router.add_api_route(
    path="/{id}",
    endpoint=DocumentosController.update,
    methods=["PUT"],
    response_model=Documento,
)

# TODO
router.add_api_route(
    path="/{id}",
    endpoint=DocumentosController.delete,
    methods=["DELETE"],
    response_model=Documento,
)
