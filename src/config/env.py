import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Environment:
    MODE = os.environ.get("ENV")


class JWT:
    SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    ALGORITHM = os.environ.get("JWT_ALGORITHM")
    EXPIRE_MINUTES = os.environ.get("JWT_EXPIRE_MINUTES")


class DataBase:
    URL_TEST = os.environ.get("DATABASE_URL_TEST")
    POSTGRES_STRING_CONNECTION = os.environ.get("POSTGRES_STRING_CONNECTION")


class Logger:
    LEVEL = os.environ.get("LOG_LEVEL")
    FILE_LINE = os.environ.get("LOG_FILE_LINE")
