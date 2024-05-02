from repositories import BaseRepository
from .schema import ObjetivoControlSchema
from .model import ObjetivoControlCreacion


class ObjetivoControlRepo(BaseRepository):
    def get(self, id: int):
        return (
            self.db.query(ObjetivoControlSchema)
            .filter(ObjetivoControlSchema.id == id)
            .first()
        )

    def get_all(self):
        return self.db.query(ObjetivoControlSchema).all()

    # def get_all_by_revision(self, revision_id: int):
    #     return self.db.query(ObjetivoControlSchema).filter(ObjetivoControlSchema.revision_id == revision_id).all()

    def create(self, objetivo: ObjetivoControlCreacion):

        db_objetivo = ObjetivoControlSchema(
            sigla=objetivo.sigla,
            nombre=objetivo.nombre,
            descripcion=objetivo.descripcion,
            padre_id=objetivo.padre_id,
        )

        self.db.add(db_objetivo)
        self.db.commit()
        self.db.refresh(db_objetivo)

        return db_objetivo

    # def update(self, id: int, objetivo: RelevamientoActualizacion):
    #     db_objetivo = self.get(id)

    #     db_objetivo.sigla = objetivo.sigla
    #     db_objetivo.nombre = objetivo.nombre
    #     db_objetivo.descripcion = objetivo.descripcion
    #     db_objetivo.padre_id = objetivo.padre_id

    #     self.db.commit()
    #     self.db.refresh(db_objetivo)

    #     return db_objetivo

    def delete(self, id: int):
        db_objetivo = self.get(id)

        print("Objeto encontrado: ", db_objetivo)

        self.db.delete(db_objetivo)
        self.db.commit()

        return db_objetivo
