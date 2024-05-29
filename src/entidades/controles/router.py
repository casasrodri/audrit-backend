from fastapi import APIRouter, status
from .controller import ControlesController
from entidades.links.controller import LinksController
from .model import Control, ResultadoBusquedaControl
from models import ResultadoBusquedaGlobal

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

# router.add_api_route(
#     path="/{control_id}/link/riesgo/{riesgo_id}",
#     endpoint=LinksController.asociar_control_riesgo,
#     methods=["POST"],
#     status_code=status.HTTP_201_CREATED,
# )

router.add_api_route(
    path="/buscarGlobal/{texto:path}",
    endpoint=ControlesController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
