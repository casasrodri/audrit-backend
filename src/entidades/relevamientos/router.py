from fastapi import APIRouter
from .controller import RelevamientosController
from .model import Relevamiento, RelevamientoNodo
from models import ResultadoBusquedaGlobal

router = APIRouter()

# Ok
router.add_api_route(
    path="",
    endpoint=RelevamientosController.get_all,
    methods=["GET"],
    response_model=list[Relevamiento],
)

# Ok
router.add_api_route(
    path="/revision/{revision_id}/nodos",
    endpoint=RelevamientosController.get_nodos_by_revision,
    methods=["GET"],
    response_model=list[RelevamientoNodo],
)

# Ok
router.add_api_route(
    path="/{id}",
    endpoint=RelevamientosController.get,
    methods=["GET"],
    response_model=Relevamiento,
)

# TODO
router.add_api_route(
    path="",
    endpoint=RelevamientosController.create,
    methods=["POST"],
    response_model=Relevamiento,
    status_code=201,
)

# TODO
router.add_api_route(
    path="/{id}",
    endpoint=RelevamientosController.update,
    methods=["PUT"],
    response_model=Relevamiento,
)

# TODO
router.add_api_route(
    path="/{id}",
    endpoint=RelevamientosController.delete,
    methods=["DELETE"],
    response_model=Relevamiento,
)

router.add_api_route(
    path="/buscarGlobal/{texto:path}",
    endpoint=RelevamientosController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
