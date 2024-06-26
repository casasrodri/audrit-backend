from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .model import AplicacionCreacion, AplicacionActualizacion
from .schema import AplicacionDB
from models import ResultadoBusquedaGlobal
from utils.helpers import extraer_medio


class AplicacionesController(BaseController):
    async def get_all(db: SqlDB):
        return db.query(AplicacionDB).all()

    async def create(db: SqlDB, aplicacion: AplicacionCreacion):
        db_aplicacion = AplicacionDB(
            nombre=aplicacion.nombre,
            descripcion=aplicacion.descripcion,
            desarrollador=aplicacion.desarrollador,
            version=aplicacion.version,
            referentes=aplicacion.referentes,
            comentarios=aplicacion.comentarios,
        )

        db.add(db_aplicacion)
        db.commit()
        db.refresh(db_aplicacion)

        return db_aplicacion

    async def update(db: SqlDB, id: int, aplicacion: AplicacionActualizacion):
        db_aplicacion = await AplicacionesController.get(db, id)

        db_aplicacion.nombre = aplicacion.nombre
        db_aplicacion.descripcion = aplicacion.descripcion
        db_aplicacion.desarrollador = aplicacion.desarrollador
        db_aplicacion.version = aplicacion.version
        db_aplicacion.referentes = aplicacion.referentes
        db_aplicacion.comentarios = aplicacion.comentarios

        db.commit()
        db.refresh(db_aplicacion)

        return db_aplicacion

    async def get(db: SqlDB, id: int, links: bool = True) -> AplicacionDB:
        aplicacion = db.query(AplicacionDB).get(id)

        if aplicacion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aplicación no encontrada.",
            )

        # Obtención de links
        if links:
            from entidades.links.controller import LinksController, EntidadLinkeable

            aplicacion.links = await LinksController.get(
                db, EntidadLinkeable.aplicacion, id
            )

        return aplicacion

    async def buscar(db: SqlDB, texto_buscado: str):
        return (
            db.query(AplicacionDB)
            .filter(
                AplicacionDB.nombre.ilike(f"%{texto_buscado}%")
                | AplicacionDB.descripcion.ilike(f"%{texto_buscado}%")
                | AplicacionDB.desarrollador.ilike(f"%{texto_buscado}%")
            )
            .all()
        )

    # async def delete(db: SqlDB, id: int):
    #     aplicacion = ControlRepo(db).delete(id)

    #     if aplicacion is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return aplicacion

    async def buscar_global(db: SqlDB, texto: str):
        encontrados = await AplicacionesController.buscar(db, texto)

        out = set()
        for apli in encontrados:

            def agregar(encontrado: str = None):
                if len(apli.descripcion) > 77:
                    descr = apli.descripcion[:77] + "..."
                else:
                    descr = apli.descripcion

                out.add(
                    ResultadoBusquedaGlobal(
                        nombre=apli.nombre,
                        texto=encontrado or descr,
                        tipo="aplicacion",
                        objeto={
                            "id": apli.id,
                        },
                    )
                )

            # Variables
            buscar = texto.replace("\n", " ").lower()
            nombre = apli.nombre.lower()
            descripcion = apli.descripcion.replace("\n", " ").lower()
            desarrollador = apli.desarrollador.replace("\n", " ").lower()
            solo_nombre = True

            # Agregación de coincidencias
            if buscar in descripcion:
                solo_nombre = False
                subtextos = extraer_medio(buscar, descripcion)
                for sub in subtextos:
                    agregar(sub)

            if buscar in desarrollador:
                solo_nombre = False
                subtextos = extraer_medio(buscar, desarrollador, longitud=68)
                for sub in subtextos:
                    agregar(f"Desarrollador: {sub}")

            if solo_nombre and buscar in nombre:
                agregar()

        return out[:10]
