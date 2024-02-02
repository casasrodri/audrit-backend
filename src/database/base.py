from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from config.env import Environment, DataBase
from utils.logger import logger

engine: Engine = None

if Environment.MODE == "dev":
    engine = create_engine(DataBase.URL_TEST, connect_args={"check_same_thread": False})

elif Environment.MODE == "production":
    engine = create_engine(DataBase.POSTGRES_STRING_CONNECTION)

SessionLocal: sessionmaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
"Cada instancia de esta clase, será una sesión de la base de datos."

BaseSchema = declarative_base()
"Base para heredar a las clases que representen tablas en la base de datos."


def init_db():
    BaseSchema.metadata.create_all(bind=engine)
    logger.info("Base de datos inicializada.")


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
