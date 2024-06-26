from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .schema import ArchivoDB
from fastapi.responses import FileResponse
from models import ResultadoBusquedaGlobal


class ArchivosController(BaseController):
    async def descargar(db: SqlDB, nombre: str):
        archivo = (
            db.query(ArchivoDB).filter(ArchivoDB.path.ilike(f"%/{nombre}")).first()
        )

        if archivo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Archivo no encontrado",
            )

        return FileResponse(
            archivo.path, filename=archivo.nombre, media_type=archivo.tipo
        )

    async def buscar_global(db: SqlDB, texto: str):
        encontrados = (
            db.query(ArchivoDB).filter(ArchivoDB.nombre.ilike(f"%{texto}%")).all()
        )

        out = set()
        for arch in encontrados:
            out.add(
                ResultadoBusquedaGlobal(
                    nombre=arch.nombre,
                    texto=f"Requerimiento: {arch.pedido.nombre}",
                    tipo="archivo",
                    objeto={
                        "requerimId": arch.pedido_id,
                    },
                )
            )

        return out[:10]
