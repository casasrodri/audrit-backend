from fastapi import APIRouter
from models import ResultadoBusquedaGlobal

from .controller import ArchivosController

router = APIRouter()

router.add_api_route(
    path="/descargar/{nombre}",
    endpoint=ArchivosController.descargar,
    methods=["GET"],
)

router.add_api_route(
    path="/buscarGlobal/{texto:path}",
    endpoint=ArchivosController.buscar_global,
    methods=["GET"],
    response_model=list[ResultadoBusquedaGlobal],
)
