from .autorizacion import autorizacion_midd
from .autenticacion import autenticacion_midd
from .console_logger import console_logger_midd
from .cors import cors_midd
from fastapi import FastAPI


# Al parecer el primero que se ejecuta es el último que se declara
def set_middlewares(app: FastAPI):
    # autorizacion_midd(app)
    # autenticacion_midd(app)
    console_logger_midd(app)
    cors_midd(app)
