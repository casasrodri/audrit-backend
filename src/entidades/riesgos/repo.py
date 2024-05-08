from repositories import BaseRepository
from .schema import RiesgoSchema
from .model import RiesgoCreacion, RiesgoActualizacion
from entidades.objetivos_control.schema import ObjetivoControlSchema
from entidades.revisiones.schema import RevisionSchema


class RiesgoRepo(BaseRepository):
    def get(self, id: int):
        return self.db.query(RiesgoSchema).filter(RiesgoSchema.id == id).first()

    def get_all(self):
        return self.db.query(RiesgoSchema).all()

    def get_all_by_revision(self, revision_id: int):
        return (
            self.db.query(RiesgoSchema)
            .filter(RiesgoSchema.revision_id == revision_id)
            .all()
        )

    def create(self, riesgo: RiesgoCreacion):

        revision = self.db.query(RevisionSchema).get(riesgo.revision_id)

        db_riesgo = RiesgoSchema(
            nombre=riesgo.nombre,
            descripcion=riesgo.descripcion,
            nivel=riesgo.nivel,
            revision=revision,
        )

        db_riesgo.objetivos_control = [
            self.db.query(ObjetivoControlSchema).get(objetivo_id)
            for objetivo_id in riesgo.objetivos_control
        ]

        self.db.add(db_riesgo)
        self.db.commit()
        self.db.refresh(db_riesgo)

        return db_riesgo

    def update(self, id: int, riesgo: RiesgoActualizacion):
        db_riesgo = self.get(id)

        db_riesgo.nombre = riesgo.nombre
        db_riesgo.descripcion = riesgo.descripcion
        db_riesgo.nivel = riesgo.nivel

        db_riesgo.objetivos_control = [
            self.db.query(ObjetivoControlSchema).get(objetivo_id)
            for objetivo_id in riesgo.objetivos_control
        ]

        self.db.commit()
        self.db.refresh(db_riesgo)

        return db_riesgo

    def buscar(self, revision_id: int, texto_buscado: str):
        return (
            self.db.query(RiesgoSchema)
            .filter(RiesgoSchema.revision_id == revision_id)
            .filter(
                RiesgoSchema.nombre.ilike(f"%{texto_buscado}%")
                | RiesgoSchema.descripcion.ilike(f"%{texto_buscado}%")
            )
            .all()
        )

    # def delete(self, id: int):
    #     db_riesgo = self.get(id)

    #     print("Objeto encontrado: ", db_riesgo)

    #     self.db.delete(db_riesgo)
    #     self.db.commit()

    #     return db_riesgo
