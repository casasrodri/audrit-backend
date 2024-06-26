from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .model import OrganigramaCreacion, OrganigramaActualizacion
from .schema import OrganigramaDB
from models import ResultadoBusquedaGlobal
from utils.helpers import extraer_medio


class OrganigramasController(BaseController):
    async def get_all(db: SqlDB):
        return db.query(OrganigramaDB).all()

    async def create(db: SqlDB, organigrama: OrganigramaCreacion):
        db_organigrama = OrganigramaDB(
            nombre=organigrama.nombre,
            descripcion=organigrama.descripcion,
            gerencia=organigrama.gerencia,
            personas=organigrama.personas,
            comentarios=organigrama.comentarios,
        )

        db.add(db_organigrama)
        db.commit()
        db.refresh(db_organigrama)

        return db_organigrama

    async def update(db: SqlDB, id: int, organigrama: OrganigramaActualizacion):
        db_organigrama = await OrganigramasController.get(db, id)

        db_organigrama.nombre = organigrama.nombre
        db_organigrama.descripcion = organigrama.descripcion
        db_organigrama.gerencia = organigrama.gerencia
        db_organigrama.personas = organigrama.personas
        db_organigrama.comentarios = organigrama.comentarios

        db.commit()
        db.refresh(db_organigrama)

        return db_organigrama

    async def get(db: SqlDB, id: int, links: bool = True) -> OrganigramaDB:
        organigrama = db.query(OrganigramaDB).get(id)

        if organigrama is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Puesto funcional no encontrado.",
            )

        # Obtención de links
        if links:
            from entidades.links.controller import LinksController, EntidadLinkeable

            organigrama.links = await LinksController.get(
                db, EntidadLinkeable.organigrama, id
            )

        return organigrama

    async def buscar(db: SqlDB, texto_buscado: str):
        return (
            db.query(OrganigramaDB)
            .filter(
                OrganigramaDB.nombre.ilike(f"%{texto_buscado}%")
                | OrganigramaDB.descripcion.ilike(f"%{texto_buscado}%")
                | OrganigramaDB.personas.ilike(f"%{texto_buscado}%")
            )
            .all()
        )

    # async def delete(db: SqlDB, id: int):
    #     organigrama = ControlRepo(db).delete(id)

    #     if organigrama is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return organigrama

    async def buscar_global(db: SqlDB, texto: str):
        encontrados = await OrganigramasController.buscar(db, texto)

        out = set()
        for org in encontrados:

            def agregar(encontrado: str = None):
                if len(org.descripcion) > 77:
                    descr = org.descripcion[:77] + "..."
                else:
                    descr = org.descripcion

                out.add(
                    ResultadoBusquedaGlobal(
                        nombre=org.nombre,
                        texto=encontrado or descr,
                        tipo="organigrama",
                        objeto={
                            "id": org.id,
                        },
                    )
                )

            # Variables
            buscar = texto.replace("\n", " ").lower()
            nombre = org.nombre.lower()
            descripcion = org.descripcion.replace("\n", " ").lower()
            personas = org.personas.replace("\n", " ").lower().replace("|", ", ")
            print(personas)
            solo_nombre = True

            # Agregación de coincidencias
            if buscar in descripcion:
                solo_nombre = False
                subtextos = extraer_medio(buscar, descripcion)
                for sub in subtextos:
                    agregar(sub)

            if buscar in personas:
                solo_nombre = False
                subtextos = extraer_medio(buscar, personas, longitud=72)
                for sub in subtextos:
                    agregar(f"Personal: {sub}")

            if solo_nombre and buscar in nombre:
                agregar()

        return out[:10]
