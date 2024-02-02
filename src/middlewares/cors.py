from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ORIGINS = ["http://localhost:5173"]


def cors_midd(app: FastAPI) -> None:
    """Aplica las póliticas de Cross-Origin Resource Sharing"""
    # print("Aplicando políticas de CORS...")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
            "Set-Cookie",
        ],
    )
