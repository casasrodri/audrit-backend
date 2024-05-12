from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .model import ControlCreacion, ControlActualizacion
from .schema import ControlDB
from entidades.revisiones.controller import RevisionesController


class ControlesController(BaseController):
    def get_all(db: SqlDB):
        return db.query(ControlDB).all()

    def get_all_by_revision(db: SqlDB, revision_id: int):
        return db.query(ControlDB).filter(ControlDB.revision_id == revision_id).all()

    def create(db: SqlDB, control: ControlCreacion):
        revision = RevisionesController.get(db, control.revision_id)

        db_control = ControlDB(
            nombre=control.nombre,
            descripcion=control.descripcion,
            ejecutor=control.ejecutor,
            oportunidad=control.oportunidad,
            periodicidad=control.periodicidad,
            automatizacion=control.automatizacion,
            revision=revision,
        )

        db.add(db_control)
        db.commit()
        db.refresh(db_control)

        return db_control

    def update(db: SqlDB, id: int, control: ControlActualizacion):
        db_control = ControlesController.get(db, id)

        db_control.nombre = control.nombre
        db_control.descripcion = control.descripcion
        db_control.ejecutor = control.ejecutor
        db_control.oportunidad = control.oportunidad
        db_control.periodicidad = control.periodicidad
        db_control.automatizacion = control.automatizacion

        db.commit()
        db.refresh(db_control)

        return db_control

    def get(db: SqlDB, id: int):
        control = db.query(ControlDB).get(id)

        if control is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Control no encontrado"
            )

        return control

    def buscar(db: SqlDB, revision_id: int, texto_buscado: str):
        return (
            db.query(ControlDB)
            .filter(ControlDB.revision_id == revision_id)
            .filter(
                ControlDB.nombre.ilike(f"%{texto_buscado}%")
                | ControlDB.descripcion.ilike(f"%{texto_buscado}%")
                | ControlDB.ejecutor.ilike(f"%{texto_buscado}%")
            )
            .all()
        )

    # def delete(db: SqlDB, id: int):
    #     control = ControlRepo(db).delete(id)

    #     if control is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return control
