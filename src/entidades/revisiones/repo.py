from repositories import BaseRepository
from .schema import RevisionSchema
from .model import RevisionCreacion, RevisionActualizacion


class RevisionesRepo(BaseRepository):
    def get(self, id: int):
        return self.db.query(RevisionSchema).filter(RevisionSchema.id == id).first()

    def get_all(self):
        return self.db.query(RevisionSchema).all()

    def get_all_auditoria(self, auditoria_id: int):
        return (
            self.db.query(RevisionSchema)
            .filter(RevisionSchema.auditoria_id == auditoria_id)
            .all()
        )

    def create(self, revision: RevisionCreacion):

        db_revision = RevisionSchema(
            sigla=revision.sigla,
            nombre=revision.nombre,
            descripcion=revision.descripcion,
            padre_id=revision.padre_id,
        )

        self.db.add(db_revision)
        self.db.commit()
        self.db.refresh(db_revision)

        return db_revision

    def update(self, id: int, revision: RevisionActualizacion):
        db_revision = self.get(id)

        db_revision.sigla = revision.sigla
        db_revision.nombre = revision.nombre
        db_revision.descripcion = revision.descripcion
        db_revision.padre_id = revision.padre_id

        self.db.commit()
        self.db.refresh(db_revision)

        return db_revision

    def delete(self, id: int):
        db_revision = self.get(id)

        print("Objeto encontrado: ", db_revision)

        self.db.delete(db_revision)
        self.db.commit()

        return db_revision
