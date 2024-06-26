from typing import Annotated

from config.env import DataBase, Environment
from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from utils.logger import logger

engine: Engine = None
motor: str = None

if Environment.MODE == "dev":
    motor = "SQLite"
    engine = create_engine(DataBase.URL_TEST, connect_args={"check_same_thread": False})

elif Environment.MODE == "production":
    motor = "PostgreSQL"
    engine = create_engine(DataBase.POSTGRES_STRING_CONNECTION)

else:
    raise ValueError("Ambiente no reconocido. Debe ser 'dev' o 'production'.")

SessionLocal: sessionmaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
"Cada instancia de esta clase, será una sesión de la base de datos."

BaseSchema = declarative_base()
"Base para heredar a las clases que representen tablas en la base de datos."


def init_db():
    BaseSchema.metadata.create_all(bind=engine)
    # print(BaseSchema.metadata.tables)
    logger.info(f"Base de datos inicializada: {motor}")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Especial Type for dependency in CRUD operations
SqlDB = Annotated[Session, Depends(get_db)]
"Proxy de una Session de SQLAlchemy, creado por SessionLocal (sessionmaker)"
