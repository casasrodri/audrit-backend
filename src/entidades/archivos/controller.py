from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .schema import ArchivoDB
from fastapi.responses import FileResponse


class ArchivosController(BaseController):

    async def descargar(db: SqlDB, nombre: str):

        archivo = (
            db.query(ArchivoDB).filter(ArchivoDB.path.ilike(f"%/{nombre}")).first()
        )

        print(nombre, archivo)

        if archivo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Archivo no encontrado",
            )

        return FileResponse(
            archivo.path, filename=archivo.nombre, media_type=archivo.tipo
        )
