from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ORIGINS = [
    "http://localhost:5173",  # Vue.js
    "http://localhost:4321",  # Astro.js
    "http://localhost:3000",  # Nuxt.js
]

# ORIGINS = ["*"]


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
