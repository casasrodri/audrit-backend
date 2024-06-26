import os

import uvicorn
from database import init_db
from fastapi import FastAPI
from middlewares import set_middlewares
from routers import set_routers

app = FastAPI()
app.title = "Audrit Backend"
app.contact = {
    "name": "Rodrigo Casas",
    "email": "cr.rodrigocasas@gmail.com",
}

set_middlewares(app)

if __name__ == "__main__":
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
