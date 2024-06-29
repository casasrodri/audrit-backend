from fastapi import APIRouter, status
from models import ResultadoBusquedaGlobal

from .controller import OrganigramasController
from .model import Organigrama, ResultadoBusquedaOrganigrama

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=OrganigramasController.get_all,
    methods=["GET"],
    response_model=list[Organigrama],
)

router.add_api_route(
    path="/{id}",
    endpoint=OrganigramasController.get,
    methods=["GET"],
    response_model=Organigrama,
)

router.add_api_route(
    path="/{id}",
    endpoint=OrganigramasController.update,
    methods=["PUT"],
    response_model=Organigrama,
)

router.add_api_route(
    path="/buscar/{texto_buscado}",
    endpoint=OrganigramasController.buscar,
    methods=["GET"],
    response_model=list[ResultadoBusquedaOrganigrama],
)

router.add_api_route(
    path="",
    endpoint=OrganigramasController.create,
    methods=["POST"],
    response_model=Organigrama,
    status_code=status.HTTP_201_CREATED,
)


# router.add_api_route(
#     path="/{id}",
#     endpoint=OrganigramasController.delete,
#     methods=["DELETE"],
#     response_model=Control,
# )

router.add_api_route(
    path="/buscarGlobal/{texto:path}",
    endpoint=OrganigramasController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
