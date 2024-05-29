from fastapi import APIRouter
from .controller import PruebasController
from .model import Prueba, ResultadoBusquedaPrueba
from models import ResultadoBusquedaGlobal

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=PruebasController.get_all,
    methods=["GET"],
    response_model=list[Prueba],
)

router.add_api_route(
    path="/revision/{revision_id}",
    endpoint=PruebasController.get_all_by_revision,
    methods=["GET"],
    response_model=list[Prueba],
)

router.add_api_route(
    path="/{id}",
    endpoint=PruebasController.get,
    methods=["GET"],
    response_model=Prueba,
)

router.add_api_route(
    path="/{id}",
    endpoint=PruebasController.update,
    methods=["PUT"],
    response_model=Prueba,
)

router.add_api_route(
    path="/revision/{revision_id}/buscar/{texto_buscado}",
    endpoint=PruebasController.buscar,
    methods=["GET"],
    response_model=list[ResultadoBusquedaPrueba],
)

# TODO
router.add_api_route(
    path="",
    endpoint=PruebasController.create,
    methods=["POST"],
    response_model=Prueba,
    status_code=201,
)

# # TODO
# router.add_api_route(
#     path="/{id}",
#     endpoint=PruebasController.delete,
#     methods=["DELETE"],
#     response_model=Control,
# )

router.add_api_route(
    path="/buscarGlobal/{texto:path}",
    endpoint=PruebasController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
