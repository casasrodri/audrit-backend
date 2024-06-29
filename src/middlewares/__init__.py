from fastapi import FastAPI

from middlewares.auth.controller import auth_middleware
from middlewares.console_logger import console_log
from middlewares.cors import cors_midd


# El primero que se ejecuta es el último que se declara
def set_middlewares(app: FastAPI):
    app.middleware("http")(auth_middleware)
    app.middleware("http")(console_log)
    cors_midd(app)
