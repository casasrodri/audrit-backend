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


set_routers(app)
init_db()
