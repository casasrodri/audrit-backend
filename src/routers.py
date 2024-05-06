from entidades.sesiones.router import router as sesiones_router
from entidades.auditorias.router import router as auditorias_router
from entidades.revisiones.router import router as revisiones_router
from entidades.relevamientos.router import router as relevamientos_router
from entidades.documentos.router import router as documentos_router
from entidades.objetivos_control.router import router as objetivos_control_router
from entidades.riesgos.router import router as riesgos_router


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

    app.include_router(
        router=objetivos_control_router,
        prefix="/api/v1/objetivos_control",
        tags=["Objetivos de control"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=riesgos_router,
        prefix="/api/v1/riesgos",
        tags=["Riesgos"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )
