from fastapi import APIRouter
from .controller import RiesgoController
from entidades.objetivos_control.model import ObjetivoControl
from .model import Riesgo, ResultadoBusquedaRiesgo
from entidades.documentos.model import Documento

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=RiesgoController.get_all,
    methods=["GET"],
    response_model=list[Riesgo],
)

router.add_api_route(
    path="/revision/{revision_id}",
    endpoint=RiesgoController.get_all_by_revision,
    methods=["GET"],
    response_model=list[Riesgo],
)

router.add_api_route(
    path="/{id}",
    endpoint=RiesgoController.get,
    methods=["GET"],
    response_model=Riesgo,
)

router.add_api_route(
    path="/{id}",
    endpoint=RiesgoController.update,
    methods=["PUT"],
    response_model=Riesgo,
)

router.add_api_route(
    path="/revision/{revision_id}/buscarRiesgo/{texto_buscado}",
    endpoint=RiesgoController.buscar,
    methods=["GET"],
    response_model=list[ResultadoBusquedaRiesgo],
)

# TODO
router.add_api_route(
    path="",
    endpoint=RiesgoController.create,
    methods=["POST"],
    response_model=Riesgo,
    status_code=201,
)

# # TODO
# router.add_api_route(
#     path="/{id}",
#     endpoint=RiesgoController.delete,
#     methods=["DELETE"],
#     response_model=Riesgo,
# )
