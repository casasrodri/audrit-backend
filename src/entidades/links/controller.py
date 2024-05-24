from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from enum import Enum

from controllers import BaseController
from database import SqlDB

from entidades.links.model import EntidadLinkeable
from entidades.links.schema import LinkDB

from entidades.controles.controller import ControlesController
from entidades.riesgos.controller import RiesgosController
from entidades.objetivos_control.controller import ObjetivosControlController
from entidades.pruebas.controller import PruebasController
from entidades.relevamientos.controller import RelevamientosController
from entidades.observaciones.controller import ObservacionesController


class RelacionExistente(HTTPException): ...


CONTROLLERS = {
    "relevamiento": RelevamientosController,
    "riesgo": RiesgosController,
    "objetivo_control": ObjetivosControlController,
    "control": ControlesController,
    "prueba": PruebasController,
    "observacion": ObservacionesController,
    "normativa": None,
    "aplicacion": None,
    "organigrama": None,
}

LINKS_VALIDOS = [
    (EntidadLinkeable.relevamiento, EntidadLinkeable.riesgo),
    (EntidadLinkeable.relevamiento, EntidadLinkeable.control),
    (EntidadLinkeable.relevamiento, EntidadLinkeable.normativa),
    (EntidadLinkeable.relevamiento, EntidadLinkeable.aplicacion),
    (EntidadLinkeable.relevamiento, EntidadLinkeable.organigrama),
    (EntidadLinkeable.riesgo, EntidadLinkeable.control),
    (EntidadLinkeable.riesgo, EntidadLinkeable.prueba),
    (EntidadLinkeable.riesgo, EntidadLinkeable.objetivo_control),
    (EntidadLinkeable.riesgo, EntidadLinkeable.normativa),
    (EntidadLinkeable.riesgo, EntidadLinkeable.aplicacion),
    (EntidadLinkeable.riesgo, EntidadLinkeable.organigrama),
    (EntidadLinkeable.control, EntidadLinkeable.prueba),
    (EntidadLinkeable.control, EntidadLinkeable.normativa),
    (EntidadLinkeable.control, EntidadLinkeable.aplicacion),
    (EntidadLinkeable.control, EntidadLinkeable.organigrama),
    (EntidadLinkeable.prueba, EntidadLinkeable.normativa),
    (EntidadLinkeable.prueba, EntidadLinkeable.aplicacion),
    (EntidadLinkeable.prueba, EntidadLinkeable.organigrama),
    (EntidadLinkeable.observacion, EntidadLinkeable.riesgo),
    (EntidadLinkeable.observacion, EntidadLinkeable.control),
    (EntidadLinkeable.observacion, EntidadLinkeable.prueba),
    (EntidadLinkeable.observacion, EntidadLinkeable.normativa),
    (EntidadLinkeable.observacion, EntidadLinkeable.aplicacion),
    (EntidadLinkeable.observacion, EntidadLinkeable.aplicacion),
    # Ejemplo prohibido: Relevamiento | Prueba
]


class AbreviaturasEntidades(Enum):
    aplicacion = "app"
    control = "ctr"
    normativa = "nor"
    objetivo_control = "oct"
    observacion = "obs"
    organigrama = "org"
    prueba = "pru"
    relevamiento = "rel"
    riesgo = "rie"


def crear_id(e1: EntidadLinkeable, i1: int, e2: EntidadLinkeable, i2: int):
    a = [
        f"{AbreviaturasEntidades[e1].value}{i1}",
        f"{AbreviaturasEntidades[e2].value}{i2}",
    ]

    return "|".join(sorted(a))


class LinksController(BaseController):
    async def create(
        db: SqlDB,
        ent1: EntidadLinkeable,
        id1: int,
        ent2: EntidadLinkeable,
        id2: int,
    ):
        if not any([(ent1, ent2) in LINKS_VALIDOS, (ent2, ent1) in LINKS_VALIDOS]):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Asociación no permitida.",
            )

        if ent1 not in CONTROLLERS or ent2 not in CONTROLLERS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entidad no encontrada.",
            )

        if ent1 == ent2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pueden relacionar dos entidades iguales.",
            )

        # Búsqueda de objetos
        obj1 = await CONTROLLERS[ent1].get(db, id1)
        obj2 = await CONTROLLERS[ent2].get(db, id2)

        print("Asociando:", obj1, obj2)
        print("Id:", crear_id(ent1, id1, ent2, id2))

        db_link = LinkDB(
            id=crear_id(ent1, id1, ent2, id2),
            ent1=ent1,
            id1=id1,
            ent2=ent2,
            id2=id2,
        )

        db.add(db_link)
        try:
            db.commit()
        except IntegrityError:
            raise RelacionExistente(
                status_code=status.HTTP_409_CONFLICT,
                detail="Relación existente.",
            )

        return db_link

    async def get(db: SqlDB, entidad: EntidadLinkeable, id: int):
        """Permite obtener todos los elementos relacionados a una entidad en particular."""

        links_db = (
            db.query(LinkDB)
            .filter(
                ((LinkDB.ent1 == entidad.name) & (LinkDB.id1 == id))
                | ((LinkDB.ent2 == entidad.name) & (LinkDB.id2 == id))
            )
            .all()
        )

        links = []
        for link in links_db:
            if link.ent1 == entidad.name:
                ent, id = link.ent2, link.id2
            else:
                ent, id = link.ent1, link.id1

            # Se busca el nombre
            obj_db = await CONTROLLERS[ent].get(db, id, links=False)

            links.append({"entidad": ent, "id": id, "nombre": obj_db.nombre})

        return links

    async def delete_all_objetivos_control(db: SqlDB, riesgo_id: int):
        entidad = EntidadLinkeable.riesgo
        oc = EntidadLinkeable.objetivo_control
        links_db = (
            db.query(LinkDB)
            .filter(
                ((LinkDB.ent1 == entidad.name) & (LinkDB.id1 == riesgo_id))
                | ((LinkDB.ent2 == entidad.name) & (LinkDB.id2 == riesgo_id))
            )
            .filter((LinkDB.ent1 == oc.name) | (LinkDB.ent2 == oc.name))
            .all()
        )

        for link in links_db:
            db.delete(link)
        db.commit()

        return links_db

    async def delete_all_links(db: SqlDB, relevamiento_id: int):
        entidad = EntidadLinkeable.relevamiento
        links_db = (
            db.query(LinkDB)
            .filter(
                ((LinkDB.ent1 == entidad.name) & (LinkDB.id1 == relevamiento_id))
                | ((LinkDB.ent2 == entidad.name) & (LinkDB.id2 == relevamiento_id))
            )
            .all()
        )

        for link in links_db:
            db.delete(link)
        db.commit()

        return links_db

    async def delete(
        db: SqlDB, ent1: EntidadLinkeable, id1: int, ent2: EntidadLinkeable, id2: int
    ):
        id_buscado = crear_id(ent1, id1, ent2, id2)
        link = db.query(LinkDB).get(id_buscado)

        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relación no encontrada.",
            )

        db.delete(link)
        db.commit()

        return link
