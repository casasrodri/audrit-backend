from fastapi import APIRouter
from .controller import ObjetivosControlController
from .model import ObjetivoControl, ObjetivoControlCreacion

router = APIRouter()

# Ok
router.add_api_route(
    path="",
    endpoint=ObjetivosControlController.get_all,
    methods=["GET"],
    response_model=list[ObjetivoControl],
)

# Ok
# router.add_api_route(
#     path="/{id}",
#     endpoint=ObjetivosControlController.get,
#     methods=["GET"],
#     response_model=Relevamiento,
# )

# TODO
router.add_api_route(
    path="",
    endpoint=ObjetivosControlController.create,
    methods=["POST"],
    response_model=ObjetivoControl,
    status_code=201,
)

# # TODO
# router.add_api_route(
#     path="/{id}",
#     endpoint=ObjetivosControlController.update,
#     methods=["PUT"],
#     response_model=Relevamiento,
# )

# # TODO
# router.add_api_route(
#     path="/{id}",
#     endpoint=ObjetivosControlController.delete,
#     methods=["DELETE"],
#     response_model=Relevamiento,
# )
