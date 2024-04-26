from fastapi import FastAPI
from middlewares import set_middlewares
from routers import set_routers
from database import init_db

app = FastAPI()

init_db()
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
    return {"Hello": "World"}


CONTROLES = [
    {
        "id": 1,
        "nombre": "Control de carga de ATMs",
        "descripcion": "El supervisor de sucursal, en conjunto con el oficial de seguridad, deberá verificar que la carga de los ATMs se realice de acuerdo a los procedimientos establecidos.",
    },
    {
        "id": 22,
        "nombre": "Control de carga del Tesoro",
        "descripcion": "El oficial de seguridad deberá verificar que la carga del tesoro se realice de acuerdo a los procedimientos establecidos.",
    },
    {
        "id": 14,
        "nombre": "Conciliaciones bancarias",
        "descripcion": "El supervisor operativo deberá verificar que las conciliaciones bancarias no den diferencias y en su caso, comunicarlas a su superior.",
    },
    {
        "id": 23,
        "nombre": "Cuentas vínculo",
        "descripcion": "El supervisor operativo deberá verificar que las cuentas vínculo queden en 0 todos los días.",
    },
]


@app.get("/api/v1/listaControles/{palabra}")
async def lista_controles(palabra: str):
    out = []
    palabra = palabra.lower()
    for c in CONTROLES:
        text = c["nombre"] + c["descripcion"]
        text = text.lower()

        if palabra in text:
            out.append(c)

    return out[:5]


@app.get("/api/v1/control/{id}")
async def info_control(id: int):
    try:
        return [c for c in CONTROLES if c["id"] == id][0]
    except:
        return {}


set_routers(app)
