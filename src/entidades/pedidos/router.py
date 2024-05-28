from fastapi import APIRouter, status
from .controller import PedidosController
from .model import Pedido, ComentarioPedido, ArchivoResumido

router = APIRouter()

router.add_api_route(
    path="",
    endpoint=PedidosController.get_all,
    methods=["GET"],
    response_model=list[Pedido],
)

# router.add_api_route(
#     path="/revision/{revision_id}",
#     endpoint=PedidosController.get_all_by_revision,
#     methods=["GET"],
#     response_model=list[Pedido],
# )

router.add_api_route(
    path="/{id}",
    endpoint=PedidosController.get,
    methods=["GET"],
    response_model=Pedido,
)

router.add_api_route(
    path="/usuario/{usuario_id}",
    endpoint=PedidosController.get_all_by_usuario,
    methods=["GET"],
    response_model=list[Pedido],
)

router.add_api_route(
    path="/{id}",
    endpoint=PedidosController.update,
    methods=["PUT"],
    response_model=Pedido,
)

# router.add_api_route(
#     path="/revision/{revision_id}/buscar/{texto_buscado}",
#     endpoint=PedidosController.buscar,
#     methods=["GET"],
#     response_model=list[ResultadoBusquedaPedido],
# )

router.add_api_route(
    path="",
    endpoint=PedidosController.create,
    methods=["POST"],
    response_model=Pedido,
    status_code=201,
)

router.add_api_route(
    path="/{id}/comentario",
    endpoint=PedidosController.create_comment,
    methods=["POST"],
    response_model=ComentarioPedido,
    status_code=201,
)

router.add_api_route(
    path="/{id}/archivos",
    endpoint=PedidosController.upload_files,
    methods=["POST"],
    response_model=list[ArchivoResumido],
    status_code=201,
)

# # TODO
# router.add_api_route(
#     path="/{id}",
#     endpoint=PedidosController.delete,
#     methods=["DELETE"],
#     response_model=Pedido,
# )

# router.add_api_route(
#     path="/{riesgo_id}/link/control/{control_id}",
#     endpoint=LinksController.asociar_control_riesgo,
#     methods=["POST"],
#     status_code=status.HTTP_201_CREATED,
# )
