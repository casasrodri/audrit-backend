from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from utils.logger import logger


def autorizacion_midd(app: FastAPI):
    # print("Inicializando middleware de autorización...")

    @app.middleware("http")
    async def autorizacion(request: Request, call_next):
        path = request.scope.get("path")
        query = request.scope.get("query_string").decode()
        user = request.scope.get("state").get("user")

        if user:
            logger.can("Autorizando al usuario: {user}...")
        else:
            logger.can("No existe usuario a autorizar.")

        # TODO esquema de validación según base de datos (VER)

        if 1 == 0:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"message": "No autorizado"},
            )

        # logger.can(f"{path=}, {query=}, {jwt=}")
        response = await call_next(request)
        return response
