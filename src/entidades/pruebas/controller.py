from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .model import PruebaCreacion, PruebaActualizacion
from .schema import PruebaDB
from entidades.revisiones.controller import RevisionesController
from models import ResultadoBusquedaGlobal
from utils.helpers import extraer_medio


class PruebasController(BaseController):
    async def get_all(db: SqlDB):
        return db.query(PruebaDB).all()

    async def get_all_by_revision(db: SqlDB, revision_id: int):
        return db.query(PruebaDB).filter(PruebaDB.revision_id == revision_id).all()

    async def create(db: SqlDB, prueba: PruebaCreacion):
        revision = await RevisionesController.get(db, prueba.revision_id)

        db_prueba = PruebaDB()
        db_prueba = PruebaDB(
            nombre=prueba.nombre,
            descripcion=prueba.descripcion,
            sector=prueba.sector,
            informe=prueba.informe,
            revision=revision,
        )

        db.add(db_prueba)
        db.commit()
        db.refresh(db_prueba)

        return db_prueba

    async def update(db: SqlDB, id: int, prueba: PruebaActualizacion):
        db_prueba = await PruebasController.get(db, id)

        db_prueba.nombre = prueba.nombre
        db_prueba.descripcion = prueba.descripcion
        db_prueba.sector = prueba.sector
        db_prueba.informe = prueba.informe

        db.commit()
        db.refresh(db_prueba)

        return db_prueba

    async def get(db: SqlDB, id: int, links: bool = True):
        prueba = db.query(PruebaDB).get(id)

        if prueba is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prueba de auditoría no encontrada.",
            )

        # Obtención de links
        if links:
            from entidades.links.controller import LinksController, EntidadLinkeable

            prueba.links = await LinksController.get(db, EntidadLinkeable.prueba, id)

        return prueba

    async def buscar(db: SqlDB, revision_id: int, texto_buscado: str):
        return (
            db.query(PruebaDB)
            .filter(PruebaDB.revision_id == revision_id)
            .filter(
                PruebaDB.nombre.ilike(f"%{texto_buscado}%")
                | PruebaDB.descripcion.ilike(f"%{texto_buscado}%")
                | PruebaDB.sector.ilike(f"%{texto_buscado}%")
                | PruebaDB.informe.ilike(f"%{texto_buscado}%")
            )
            .all()
        )

    # async def delete(db: SqlDB, id: int):
    #     control = ControlRepo(db).delete(id)

    #     if control is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return control

    async def buscar_global(db: SqlDB, texto: str):
        encontrados = (
            db.query(PruebaDB)
            .filter(
                PruebaDB.nombre.ilike(f"%{texto}%")
                | PruebaDB.descripcion.ilike(f"%{texto}%")
                | PruebaDB.informe.ilike(f"%{texto}%")
            )
            .all()
        )

        out = set()
        for pru in encontrados:
            rev = pru.revision
            aud = rev.auditoria

            def agregar(encontrado: str = None):
                if len(pru.descripcion) > 77:
                    descr = pru.descripcion[:77] + "..."
                else:
                    descr = pru.descripcion

                out.add(
                    ResultadoBusquedaGlobal(
                        nombre=pru.nombre,
                        texto=encontrado or descr,
                        tipo="prueba",
                        objeto={
                            "siglaAudit": aud.sigla,
                            "siglaRev": rev.sigla,
                            "id": pru.id,
                        },
                    )
                )

            # Variables
            buscar = texto.replace("\n", " ").lower()
            nombre = pru.nombre.lower()
            descripcion = pru.descripcion.replace("\n", " ").lower()
            informe = pru.informe.replace("\n", " ").lower()
            solo_nombre = True

            # Agregación de coincidencias
            if buscar in descripcion:
                solo_nombre = False
                subtextos = extraer_medio(buscar, descripcion)
                for sub in subtextos:
                    agregar(sub)

            if buscar in informe:
                solo_nombre = False
                subtextos = extraer_medio(buscar, informe, longitud=70)
                for sub in subtextos:
                    agregar(f"Informe: {sub.upper()}")

            if solo_nombre and buscar in nombre:
                agregar()

        return list(out)[:10]
