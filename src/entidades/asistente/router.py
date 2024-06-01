from fastapi import APIRouter
from .controller import consultar_asistente, actualizar_contenido

router = APIRouter()

router.add_api_websocket_route(
    path="/ws",
    endpoint=consultar_asistente,
)

router.add_api_route(
    path="/actualizarContenido",
    endpoint=actualizar_contenido,
)
