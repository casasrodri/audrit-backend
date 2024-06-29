from fastapi import APIRouter, status
from models import ResultadoBusquedaGlobal

from .controller import NormativasController
from .model import Normativa, ResultadoBusquedaNormativa

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=NormativasController.get_all,
    methods=["GET"],
    response_model=list[Normativa],
)

router.add_api_route(
    path="/{id}",
    endpoint=NormativasController.get,
    methods=["GET"],
    response_model=Normativa,
)

router.add_api_route(
    path="/{id}",
    endpoint=NormativasController.update,
    methods=["PUT"],
    response_model=Normativa,
)

router.add_api_route(
    path="/buscar/{texto_buscado}",
    endpoint=NormativasController.buscar,
    methods=["GET"],
    response_model=list[ResultadoBusquedaNormativa],
)

router.add_api_route(
    path="",
    endpoint=NormativasController.create,
    methods=["POST"],
    response_model=Normativa,
    status_code=status.HTTP_201_CREATED,
)


# router.add_api_route(
#     path="/{id}",
#     endpoint=NormativasController.delete,
#     methods=["DELETE"],
#     response_model=Control,
# )

router.add_api_route(
    path="/buscarGlobal/{texto:path}",
    endpoint=NormativasController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
