from fastapi import APIRouter
from .controller import ObservacionesController
from .model import Observacion, ResultadoBusquedaObservacion
from models import ResultadoBusquedaGlobal

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=ObservacionesController.get_all,
    methods=["GET"],
    response_model=list[Observacion],
)

router.add_api_route(
    path="/revision/{revision_id}",
    endpoint=ObservacionesController.get_all_by_revision,
    methods=["GET"],
    response_model=list[Observacion],
)

router.add_api_route(
    path="/{id}",
    endpoint=ObservacionesController.get,
    methods=["GET"],
    response_model=Observacion,
)

router.add_api_route(
    path="/{id}",
    endpoint=ObservacionesController.update,
    methods=["PUT"],
    response_model=Observacion,
)

router.add_api_route(
    path="/revision/{revision_id}/buscar/{texto_buscado}",
    endpoint=ObservacionesController.buscar,
    methods=["GET"],
    response_model=list[ResultadoBusquedaObservacion],
)

router.add_api_route(
    path="",
    endpoint=ObservacionesController.create,
    methods=["POST"],
    response_model=Observacion,
    status_code=201,
)

# # TODO
# router.add_api_route(
#     path="/{id}",
#     endpoint=ObservacionesController.delete,
#     methods=["DELETE"],
#     response_model=Observacion,
# )

# router.add_api_route(
#     path="/{riesgo_id}/link/control/{control_id}",
#     endpoint=LinksController.asociar_control_riesgo,
#     methods=["POST"],
#     status_code=status.HTTP_201_CREATED,
# )

router.add_api_route(
    path="/buscarGlobal/{texto:path}",
    endpoint=ObservacionesController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
