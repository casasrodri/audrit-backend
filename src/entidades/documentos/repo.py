from repositories import BaseRepository
from .schema import DocumentoSchema
from .model import DocumentoCreacion, DocumentoActualizacion


class DocumentosRepo(BaseRepository):
    def get(self, id: int):
        return self.db.query(DocumentoSchema).filter(DocumentoSchema.id == id).first()

    def get_all(self):
        return self.db.query(DocumentoSchema).all()

    def get_by_relevamiento(self, relevamiento_id: int):
        return (
            self.db.query(DocumentoSchema)
            .filter(DocumentoSchema.relevamiento_id == relevamiento_id)
            .first()
        )

    def create(self, documento: DocumentoCreacion):
        print(documento)

        db_documento = DocumentoSchema(
            relevamiento_id=documento.relevamiento_id,
            contenido=documento.contenido,
        )

        self.db.add(db_documento)
        self.db.commit()
        self.db.refresh(db_documento)

        return db_documento

    def update(self, id: int, documento: DocumentoActualizacion):
        db_documento = self.get(id)

        db_documento.relevamiento_id = documento.relevamiento_id
        db_documento.contenido = documento.contenido

        self.db.commit()
        self.db.refresh(db_documento)

        return db_documento

    def delete(self, id: int):
        db_documento = self.get(id)

        print("Objeto encontrado: ", db_documento)

        self.db.delete(db_documento)
        self.db.commit()

        return db_documento
