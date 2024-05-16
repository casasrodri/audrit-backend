from fastapi import APIRouter, status
from .controller import LinksController

router = APIRouter()

router.add_api_route(
    path="/control/{control_id}/riesgo/{riesgo_id}",
    endpoint=LinksController.asociar_control_riesgo,
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
)

router.add_api_route(
    path="/riesgo/{riesgo_id}/control/{control_id}",
    endpoint=LinksController.asociar_control_riesgo,
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
)
