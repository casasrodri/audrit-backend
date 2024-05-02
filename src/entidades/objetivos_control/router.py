from fastapi import APIRouter
from .controller import ObjetivoControlController
from .model import ObjetivoControl, ObjetivoControlCreacion

router = APIRouter()

# Ok
router.add_api_route(
    path="",
    endpoint=ObjetivoControlController.get_all,
    methods=["GET"],
    response_model=list[ObjetivoControl],
)

# Ok
# router.add_api_route(
#     path="/{id}",
#     endpoint=ObjetivoControlController.get,
#     methods=["GET"],
#     response_model=Relevamiento,
# )

# TODO
router.add_api_route(
    path="",
    endpoint=ObjetivoControlController.create,
    methods=["POST"],
    response_model=ObjetivoControl,
    status_code=201,
)

# # TODO
# router.add_api_route(
#     path="/{id}",
#     endpoint=ObjetivoControlController.update,
#     methods=["PUT"],
#     response_model=Relevamiento,
# )

# # TODO
# router.add_api_route(
#     path="/{id}",
#     endpoint=ObjetivoControlController.delete,
#     methods=["DELETE"],
#     response_model=Relevamiento,
# )
