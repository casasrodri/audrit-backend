from fastapi import FastAPI
from middlewares import set_middlewares
from routers import set_routers
from database import init_db
import os

app = FastAPI()


set_middlewares(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        port=8000,
        reload=True,
        access_log=True,
        host="0.0.0.0",
    )


@app.get("/")
async def home():
    return {"PID": os.getpid()}


from database import SqlDB
from entidades.riesgos.controller import RiesgosController
from entidades.riesgos.model import Riesgo

from entidades.documentos.controller import DocumentosController
from entidades.documentos.model import Documento


@app.get("/riesgo/{id}")
async def test(db: SqlDB, id: int = 5) -> Riesgo:
    return RiesgosController.get(db, id)


@app.get("/documento/{id}")
async def test(db: SqlDB, id: int = 0) -> Documento:
    return DocumentosController.get(db, id)


set_routers(app)
init_db()
