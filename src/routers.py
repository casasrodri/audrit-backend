from entidades.ciclos.router import router as ciclos_router
from entidades.auditorias.router import router as auditorias_router
from entidades.mascotas.router import router as mascotas_router
from entidades.sesiones.router import router as sesiones_router


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
        router=mascotas_router,
        # prefix="/usuarios",
        tags=["Mascotas"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=ciclos_router,
        prefix="/api/v1/ciclos",
        tags=["Ciclos"],
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
