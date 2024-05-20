from fastapi import APIRouter, status
from .controller import LinksController
from .model import ElementoLinkeado

router = APIRouter()

router.add_api_route(
    path="/{ent1}/{id1}/{ent2}/{id2}",
    endpoint=LinksController.create,
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
)


router.add_api_route(
    path="/{entidad}/{id}",
    endpoint=LinksController.get,
    methods=["GET"],
    response_model=list[ElementoLinkeado],
)

router.add_api_route(
    path="/{ent1}/{id1}/{ent2}/{id2}",
    endpoint=LinksController.delete,
    methods=["DELETE"],
)
