from fastapi import APIRouter
from .controller import UsuariosController
from .model import UsuarioOut
from models import ResultadoBusquedaGlobal

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=UsuariosController.get_all,
    methods=["GET"],
    response_model=list[UsuarioOut],
)

router.add_api_route(
    path="/{id}",
    endpoint=UsuariosController.get_by_id,
    methods=["GET"],
    response_model=UsuarioOut,
)

router.add_api_route(
    path="/email/{email}",
    endpoint=UsuariosController.get_by_email,
    methods=["GET"],
    response_model=UsuarioOut,
)

router.add_api_route(
    path="",
    endpoint=UsuariosController.create,
    methods=["POST"],
    response_model=UsuarioOut,
    status_code=201,
)

router.add_api_route(
    path="/buscar/{texto_buscado}",
    endpoint=UsuariosController.buscar,
    methods=["GET"],
    response_model=list[UsuarioOut],
)


# router.add_api_route(
#     path="/{id}",
#     endpoint=RevisionesController.update,
#     methods=["PUT"],
#     response_model=Revision,
# )

# router.add_api_route(
#     path="/{id}",
#     endpoint=RevisionesController.delete,
#     methods=["DELETE"],
#     response_model=Revision,
# )

router.add_api_route(
    path="/buscarGlobal/{texto:path}",
    endpoint=UsuariosController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
