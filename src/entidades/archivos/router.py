from fastapi import APIRouter
from .controller import ArchivosController
from models import ResultadoBusquedaGlobal

router = APIRouter()

router.add_api_route(
    path="/descargar/{nombre}",
    endpoint=ArchivosController.descargar,
    methods=["GET"],
)

router.add_api_route(
    path="/buscarGlobal/{texto}",
    endpoint=ArchivosController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
