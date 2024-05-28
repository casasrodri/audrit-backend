from fastapi import FastAPI

# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

ORIGINS = [
    "http://localhost:5173",  # Vue.js
    "http://localhost:4321",  # Astro.js
    "http://localhost:3000",  # Nuxt.js
    # "http://192.168.1.3:5173",  # Galaxy
    # "http://192.168.1.24:5173",  # Galaxy
    "*",  # Cualquier origen
]

# ORIGINS = ["*"]

import socket

nuevos_orig = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]
ORIGINS = [f"http://{ip}:5173" for ip in nuevos_orig if ":" not in ip]
ORIGINS.append("http://localhost:5173")
# ORIGINS.append("https://npmqbzfq-5173.brs.devtunnels.ms")


def cors_midd(app: FastAPI) -> None:
    """Aplica las póliticas de Cross-Origin Resource Sharing"""
    # print("Aplicando políticas de CORS...")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # class DebugCORSMiddleware(BaseHTTPMiddleware):
    #     """Permite el acceso a la API desde cualquier origen, método y cabecera."""

    #     async def dispatch(self, request: Request, call_next):
    #         response = await call_next(request)

    #         origin = request.headers.get("origin")
    #         if origin:
    #             response.headers["Access-Control-Allow-Origin"] = origin
    #             response.headers["Vary"] = "Origin"

    #         return response

    # # Apply custom CORS middleware
    # # app.add_middleware(DebugCORSMiddleware)
