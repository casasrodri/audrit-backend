from entidades.sesiones.router import router as sesiones_router
from entidades.auditorias.router import router as auditorias_router
from entidades.revisiones.router import router as revisiones_router
from entidades.relevamientos.router import router as relevamientos_router
from entidades.documentos.router import router as documentos_router


def set_routers(app):
    app.include_router(
        router=sesiones_router,
        prefix="/api/v1",
        tags=["Sesiones"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=auditorias_router,
        prefix="/api/v1/auditorias",
        tags=["Auditorías"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=revisiones_router,
        prefix="/api/v1/revisiones",
        tags=["Revisiones"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=relevamientos_router,
        prefix="/api/v1/relevamientos",
        tags=["Relevamientos"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=documentos_router,
        prefix="/api/v1/documentos",
        tags=["Documentos"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )
