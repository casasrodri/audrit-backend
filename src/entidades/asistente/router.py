from fastapi import APIRouter
from .controller import (
    consultar_asistente,
    contar_cantidad_pendientes,
    sincronizar,
)

router = APIRouter()

router.add_api_websocket_route(
    path="/ws",
    endpoint=consultar_asistente,
)

router.add_api_route(
    path="/contarCantidadPendientes",
    endpoint=contar_cantidad_pendientes,
)

router.add_api_route(
    path="/sincronizar",
    endpoint=sincronizar,
)
