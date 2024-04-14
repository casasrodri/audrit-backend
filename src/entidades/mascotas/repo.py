from repositories import BaseRepository
from .schema import MascotaSchema
from .model import MascotaCreacion


class MascotasRepo(BaseRepository):
    def get(self, pet_id: int):
        return self.db.query(MascotaSchema).filter(MascotaSchema.id == pet_id).first()

    def get_by_email(self, email: str):
        return self.db.query(MascotaSchema).filter(MascotaSchema.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(MascotaSchema).offset(skip).limit(limit).all()

    def create(self, pet: MascotaCreacion):
        fake_hashed_password = pet.password + ":::::notreallyhashed"

        db_pet = MascotaSchema(email=pet.email, hashed_password=fake_hashed_password)

        self.db.add(db_pet)
        self.db.commit()
        self.db.refresh(db_pet)

        return db_pet
