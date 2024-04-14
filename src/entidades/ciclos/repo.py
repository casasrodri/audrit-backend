from repositories import BaseRepository
from .schema import CicloSchema
from .model import CicloCreacion, CicloActualizacion


class CiclosRepo(BaseRepository):
    def get(self, id: int):
        return self.db.query(CicloSchema).filter(CicloSchema.id == id).first()

    def get_all(self):
        return self.db.query(CicloSchema).all()

    def create(self, ciclo: CicloCreacion):

        db_ciclo = CicloSchema(
            sigla=ciclo.sigla,
            nombre=ciclo.nombre,
            descripcion=ciclo.descripcion,
            padre_id=ciclo.padre_id,
        )

        self.db.add(db_ciclo)
        self.db.commit()
        self.db.refresh(db_ciclo)

        return db_ciclo

    def update(self, id: int, ciclo: CicloActualizacion):
        db_ciclo = self.get(id)

        db_ciclo.sigla = ciclo.sigla
        db_ciclo.nombre = ciclo.nombre
        db_ciclo.descripcion = ciclo.descripcion
        db_ciclo.padre_id = ciclo.padre_id

        self.db.commit()
        self.db.refresh(db_ciclo)

        return db_ciclo

    def delete(self, id: int):
        db_ciclo = self.get(id)

        print("Objeto encontrado: ", db_ciclo)

        self.db.delete(db_ciclo)
        self.db.commit()

        return db_ciclo
