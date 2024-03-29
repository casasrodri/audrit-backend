from .base import BaseController
from fastapi import HTTPException
from database.base import SqlDB
from repositories.mascotas import MascotasRepo
from models.mascotas import MascotaCreacion


class MascotasController(BaseController):
    def get_all(db: SqlDB, skip: int = 0, limit: int = 100):
        return MascotasRepo(db).get_all(skip=skip, limit=limit)

    def create(db: SqlDB, pet: MascotaCreacion):
        db_pet = MascotasRepo(db).get_by_email(email=pet.email)

        if db_pet:
            # TODO: Crear una clase personalizada de Errores
            raise HTTPException(status_code=400, detail="Email already registered")

        return MascotasRepo(db).create(pet)
