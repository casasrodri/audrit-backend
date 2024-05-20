from fastapi import APIRouter, status
from .controller import RiesgosController
from entidades.links.controller import LinksController
from .model import Riesgo, ResultadoBusquedaRiesgo, Riesgo

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=RiesgosController.get_all,
    methods=["GET"],
    response_model=list[Riesgo],
)

router.add_api_route(
    path="/revision/{revision_id}",
    endpoint=RiesgosController.get_all_by_revision,
    methods=["GET"],
    response_model=list[Riesgo],
)

router.add_api_route(
    path="/{id}",
    endpoint=RiesgosController.get,
    methods=["GET"],
    response_model=Riesgo,
)

router.add_api_route(
    path="/{id}",
    endpoint=RiesgosController.update,
    methods=["PUT"],
    response_model=Riesgo,
)

router.add_api_route(
    path="/revision/{revision_id}/buscar/{texto_buscado}",
    endpoint=RiesgosController.buscar,
    methods=["GET"],
    response_model=list[ResultadoBusquedaRiesgo],
)

# TODO
router.add_api_route(
    path="",
    endpoint=RiesgosController.create,
    methods=["POST"],
    response_model=Riesgo,
    status_code=201,
)

# # TODO
# router.add_api_route(
#     path="/{id}",
#     endpoint=RiesgosController.delete,
#     methods=["DELETE"],
#     response_model=Riesgo,
# )

# router.add_api_route(
#     path="/{riesgo_id}/link/control/{control_id}",
#     endpoint=LinksController.asociar_control_riesgo,
#     methods=["POST"],
#     status_code=status.HTTP_201_CREATED,
# )
