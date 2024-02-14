from .base import BaseRepository
from database.schemas.ciclo import CicloSchema
from models.ciclos import CicloCreacion


class CiclosRepo(BaseRepository):
    def get(self, ciclo_id: int):
        return self.db.query(CicloSchema).filter(CicloSchema.id == ciclo_id).first()

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
