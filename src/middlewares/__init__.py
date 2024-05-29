from .autorizacion import autorizacion_midd
from .autenticacion import autenticacion
from .console_logger import console_log
from .cors import cors_midd
from fastapi import FastAPI


# El primero que se ejecuta es el último que se declara
def set_middlewares(app: FastAPI):
    # app.middleware("http")(autorizacion)
    app.middleware("http")(autenticacion)
    app.middleware("http")(console_log)
    cors_midd(app)
