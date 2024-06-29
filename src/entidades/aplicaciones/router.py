from fastapi import APIRouter, status
from models import ResultadoBusquedaGlobal

from .controller import AplicacionesController
from .model import Aplicacion, ResultadoBusquedaAplicacion

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=AplicacionesController.get_all,
    methods=["GET"],
    response_model=list[Aplicacion],
)

router.add_api_route(
    path="/{id}",
    endpoint=AplicacionesController.get,
    methods=["GET"],
    response_model=Aplicacion,
)

router.add_api_route(
    path="/{id}",
    endpoint=AplicacionesController.update,
    methods=["PUT"],
    response_model=Aplicacion,
)

router.add_api_route(
    path="/buscar/{texto_buscado}",
    endpoint=AplicacionesController.buscar,
    methods=["GET"],
    response_model=list[ResultadoBusquedaAplicacion],
)

router.add_api_route(
    path="",
    endpoint=AplicacionesController.create,
    methods=["POST"],
    response_model=Aplicacion,
    status_code=status.HTTP_201_CREATED,
)


# router.add_api_route(
#     path="/{id}",
#     endpoint=AplicacionesController.delete,
#     methods=["DELETE"],
#     response_model=Control,
# )

router.add_api_route(
    path="/buscarGlobal/{texto:path}",
    endpoint=AplicacionesController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
