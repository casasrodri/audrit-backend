from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .model import NormativaCreacion, NormativaActualizacion
from .schema import NormativaDB
from models import ResultadoBusquedaGlobal
from utils.helpers import extraer_medio


class NormativasController(BaseController):
    async def get_all(db: SqlDB):
        return db.query(NormativaDB).all()

    async def create(db: SqlDB, normativa: NormativaCreacion):
        db_normativa = NormativaDB(
            nomenclatura=normativa.nomenclatura,
            nombre=normativa.nombre,
            descripcion=normativa.descripcion,
            tipo=normativa.tipo,
            emisor=normativa.emisor,
            fecha_emision=normativa.fecha_emision,
            fecha_actualizacion=normativa.fecha_actualizacion,
            comentarios=normativa.comentarios,
        )

        db.add(db_normativa)
        db.commit()
        db.refresh(db_normativa)

        return db_normativa

    async def update(db: SqlDB, id: int, normativa: NormativaActualizacion):
        db_normativa = await NormativasController.get(db, id)

        db_normativa.nomenclatura = normativa.nomenclatura
        db_normativa.nombre = normativa.nombre
        db_normativa.descripcion = normativa.descripcion
        db_normativa.tipo = normativa.tipo
        db_normativa.emisor = normativa.emisor
        db_normativa.fecha_emision = normativa.fecha_emision
        db_normativa.fecha_actualizacion = normativa.fecha_actualizacion
        db_normativa.comentarios = normativa.comentarios

        db.commit()
        db.refresh(db_normativa)

        return db_normativa

    async def get(db: SqlDB, id: int, links: bool = True) -> NormativaDB:
        normativa = db.query(NormativaDB).get(id)

        if normativa is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Normativa no encontrada."
            )

        # Obtención de links
        if links:
            from entidades.links.controller import LinksController, EntidadLinkeable

            normativa.links = await LinksController.get(
                db, EntidadLinkeable.normativa, id
            )

        return normativa

    async def buscar(db: SqlDB, texto_buscado: str):
        return (
            db.query(NormativaDB)
            .filter(
                NormativaDB.nomenclatura.ilike(f"%{texto_buscado}%")
                | NormativaDB.nombre.ilike(f"%{texto_buscado}%")
                | NormativaDB.descripcion.ilike(f"%{texto_buscado}%")
            )
            .all()
        )

    # async def delete(db: SqlDB, id: int):
    #     normativa = ControlRepo(db).delete(id)

    #     if normativa is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return normativa

    async def buscar_global(db: SqlDB, texto: str):
        encontrados = await NormativasController.buscar(db, texto)

        out = set()
        for nor in encontrados:

            def agregar(encontrado: str = None):
                if len(nor.descripcion) > 77:
                    descr = nor.descripcion[:77] + "..."
                else:
                    descr = nor.descripcion

                out.add(
                    ResultadoBusquedaGlobal(
                        nombre=f"{nor.nomenclatura} - {nor.nombre}",
                        texto=encontrado or descr,
                        tipo="normativa",
                        objeto={
                            "id": nor.id,
                        },
                    )
                )

            # Variables
            buscar = texto.replace("\n", " ").lower()
            nombre = nor.nombre.lower() + " " + nor.nomenclatura.lower()
            descripcion = nor.descripcion.replace("\n", " ").lower()

            # Agregación de coincidencias
            if buscar in descripcion:
                subtextos = extraer_medio(buscar, descripcion)
                for sub in subtextos:
                    agregar(sub)
            else:
                if buscar in nombre:
                    agregar()

        return out
