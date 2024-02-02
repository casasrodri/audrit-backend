from fastapi import APIRouter
from controllers.mascotas import MascotasController
from models.mascotas import Mascota

router = APIRouter()

router.add_api_route(
    path="/mascotas",
    endpoint=MascotasController.get_all,
    methods=["GET"],
    response_model=list[Mascota],
)

router.add_api_route(
    path="/mascotas",
    endpoint=MascotasController.create,
    methods=["POST"],
    response_model=Mascota,
)
