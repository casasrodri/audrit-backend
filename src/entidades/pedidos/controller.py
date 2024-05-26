from datetime import datetime
from fastapi import HTTPException, status, UploadFile
from controllers import BaseController
from database import SqlDB
from .model import PedidoCreacion, ComentarioPedidoCreacion
from .schema import PedidoDB, ComentariosPedidosDB
from entidades.usuarios.controller import UsuariosController
from entidades.archivos.schema import ArchivoDB


def guardar_archivo(archivo: UploadFile):
    ya = datetime.now().strftime("%Y%m%d%H%M%S")
    hexa = hex(int(ya)).lstrip("0x")
    path = f"uploads/{hexa}_{archivo.filename}"

    with open(path, "wb") as f:
        f.write(archivo.file.read())

    return path


class PedidosController(BaseController):
    async def get_all(db: SqlDB):  # OK
        return db.query(PedidoDB).all()

    async def get(db: SqlDB, id: int):  # Ok
        pedido = db.query(PedidoDB).get(id)

        if pedido is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido no encontrado",
            )

        return pedido

    async def create(db: SqlDB, pedido: PedidoCreacion):  # OK

        user_creador = await UsuariosController.get_by_id(db, pedido.creador_id)
        user_destinatario = await UsuariosController.get_by_id(
            db, pedido.destinatario_id
        )

        db_pedido = PedidoDB(
            nombre=pedido.nombre,
            descripcion=pedido.descripcion,
            estado=pedido.estado,
            fecha_vencimiento=pedido.fecha_vencimiento,
            creador=user_creador,
            destinatario=user_destinatario,
        )

        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)

        return db_pedido

    async def create_comment(
        db: SqlDB, id: int, comentario: ComentarioPedidoCreacion
    ):  # OK
        pedido = await PedidosController.get(db, id)
        user = await UsuariosController.get_by_id(db, comentario.usuario_id)

        db_comentario = ComentariosPedidosDB(
            momento=datetime.now(), pedido=pedido, usuario=user, texto=comentario.texto
        )

        db.add(db_comentario)
        db.commit()
        db.refresh(db_comentario)

        return db_comentario

    async def upload_files(db: SqlDB, id: int, archivos: list[UploadFile]):
        # <body>
        # <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
        # <input name="files" type="file" multiple>
        # <input type="submit">
        # </form>
        # </body>

        pedido = await PedidosController.get(db, id)

        subidos: list[ArchivoDB] = []
        for archivo in archivos:
            db_archivo = ArchivoDB(
                nombre=archivo.filename,
                bytes=archivo.size,
                tipo=archivo.headers["content-type"],
                path=guardar_archivo(archivo),
                pedido=pedido,
            )

            db.add(db_archivo)
            db.commit()
            db.refresh(db_archivo)

            subidos.append(db_archivo)

        return subidos
