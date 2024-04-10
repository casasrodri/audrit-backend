from fastapi import APIRouter
from controllers.ciclos import CiclosController
from models.ciclos import Ciclo, CicloNodo

router = APIRouter()

router.add_api_route(
    path="/",
    endpoint=CiclosController.get_all,
    methods=["GET"],
    response_model=list[Ciclo],
)

router.add_api_route(
    path="/nodos",
    endpoint=CiclosController.get_nodos,
    methods=["GET"],
    response_model=list[CicloNodo],
)

router.add_api_route(
    path="/",
    endpoint=CiclosController.create,
    methods=["POST"],
    response_model=Ciclo,
    status_code=201,
)

router.add_api_route(
    path="/{id}",
    endpoint=CiclosController.update,
    methods=["PUT"],
    response_model=Ciclo,
)

router.add_api_route(
    path="/{id}",
    endpoint=CiclosController.get,
    methods=["GET"],
    response_model=Ciclo,
)

router.add_api_route(
    path="/{id}",
    endpoint=CiclosController.delete,
    methods=["DELETE"],
    response_model=Ciclo,
)
