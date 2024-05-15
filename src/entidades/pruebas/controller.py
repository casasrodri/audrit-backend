from fastapi import HTTPException, status
from controllers import BaseController
from database import SqlDB
from .model import PruebaCreacion, PruebaActualizacion
from .schema import PruebaDB
from entidades.revisiones.controller import RevisionesController


class PruebasController(BaseController):
    def get_all(db: SqlDB):
        return db.query(PruebaDB).all()

    def get_all_by_revision(db: SqlDB, revision_id: int):
        return db.query(PruebaDB).filter(PruebaDB.revision_id == revision_id).all()

    def create(db: SqlDB, control: PruebaCreacion):
        revision = RevisionesController.get(db, control.revision_id)

        db_prueba = PruebaDB()
        db_prueba = PruebaDB(
            nombre=control.nombre,
            descripcion=control.descripcion,
            sector=control.sector,
            informe=control.informe,
            revision=revision,
        )

        db.add(db_prueba)
        db.commit()
        db.refresh(db_prueba)

        return db_prueba

    def update(db: SqlDB, id: int, control: PruebaActualizacion):
        db_prueba = PruebasController.get(db, id)

        db_prueba.nombre = control.nombre
        db_prueba.descripcion = control.descripcion
        db_prueba.sector = control.sector
        db_prueba.informe = control.informe

        db.commit()
        db.refresh(db_prueba)

        return db_prueba

    def get(db: SqlDB, id: int):
        control = db.query(PruebaDB).get(id)

        if control is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prueba de auditoría no encontrada.",
            )

        return control

    def buscar(db: SqlDB, revision_id: int, texto_buscado: str):
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

    # def delete(db: SqlDB, id: int):
    #     control = ControlRepo(db).delete(id)

    #     if control is None:
    #         raise HTTPException(status_code=404, detail="Relevamiento no encontrado")

    #     return control
