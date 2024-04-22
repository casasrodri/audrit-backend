from repositories import BaseRepository
from .schema import RelevamientoSchema
from .model import RelevamientoCreacion, RelevamientoActualizacion


class RelevamientosRepo(BaseRepository):
    def get(self, id: int):
        return (
            self.db.query(RelevamientoSchema)
            .filter(RelevamientoSchema.id == id)
            .first()
        )

    def get_all_by_revision(self, revision_id: int):
        return self.db.query(RelevamientoSchema).filter(RelevamientoSchema.revision_id == revision_id).all()

    def create(self, relevamiento: RelevamientoCreacion):

        db_relevamiento = RelevamientoSchema(
            sigla=relevamiento.sigla,
            nombre=relevamiento.nombre,
            descripcion=relevamiento.descripcion,
            padre_id=relevamiento.padre_id,
        )

        self.db.add(db_relevamiento)
        self.db.commit()
        self.db.refresh(db_relevamiento)

        return db_relevamiento

    def update(self, id: int, relevamiento: RelevamientoActualizacion):
        db_relevamiento = self.get(id)

        db_relevamiento.sigla = relevamiento.sigla
        db_relevamiento.nombre = relevamiento.nombre
        db_relevamiento.descripcion = relevamiento.descripcion
        db_relevamiento.padre_id = relevamiento.padre_id

        self.db.commit()
        self.db.refresh(db_relevamiento)

        return db_relevamiento

    def delete(self, id: int):
        db_relevamiento = self.get(id)

        print("Objeto encontrado: ", db_relevamiento)

        self.db.delete(db_relevamiento)
        self.db.commit()

        return db_relevamiento
