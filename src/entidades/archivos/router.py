from fastapi import APIRouter
from .controller import ArchivosController

router = APIRouter()

router.add_api_route(
    path="/descargar/{nombre}",
    endpoint=ArchivosController.descargar,
    methods=["GET"],
)
