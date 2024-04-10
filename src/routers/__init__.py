from . import sesiones
from . import mascotas
from . import ciclos
from . import auditorias


def set_routers(app):
    app.include_router(
        router=sesiones.router,
        prefix="/api/v1",
        tags=["Sesiones"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=mascotas.router,
        # prefix="/usuarios",
        tags=["Mascotas"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=ciclos.router,
        prefix="/api/v1/ciclos",
        tags=["Ciclos"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=auditorias.router,
        prefix="/api/v1/auditorias",
        tags=["Auditorías"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )
