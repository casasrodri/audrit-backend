from fastapi import APIRouter
from .controller import ControlesController
from .model import Control, ResultadoBusquedaControl

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=ControlesController.get_all,
    methods=["GET"],
    response_model=list[Control],
)

router.add_api_route(
    path="/revision/{revision_id}",
    endpoint=ControlesController.get_all_by_revision,
    methods=["GET"],
    response_model=list[Control],
)

router.add_api_route(
    path="/{id}",
    endpoint=ControlesController.get,
    methods=["GET"],
    response_model=Control,
)

router.add_api_route(
    path="/{id}",
    endpoint=ControlesController.update,
    methods=["PUT"],
    response_model=Control,
)

router.add_api_route(
    path="/revision/{revision_id}/buscar/{texto_buscado}",
    endpoint=ControlesController.buscar,
    methods=["GET"],
    response_model=list[ResultadoBusquedaControl],
)

# TODO
router.add_api_route(
    path="",
    endpoint=ControlesController.create,
    methods=["POST"],
    response_model=Control,
    status_code=201,
)

# # TODO
# router.add_api_route(
#     path="/{id}",
#     endpoint=ControlesController.delete,
#     methods=["DELETE"],
#     response_model=Control,
# )