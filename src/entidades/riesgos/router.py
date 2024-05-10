from fastapi import APIRouter
from .controller import RiesgosController
from entidades.objetivos_control.model import ObjetivoControl
from .model import Riesgo, ResultadoBusquedaRiesgo
from entidades.documentos.model import Documento

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
    path="/revision/{revision_id}/buscarRiesgo/{texto_buscado}",
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
