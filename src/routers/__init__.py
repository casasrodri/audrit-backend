from . import sesiones
from . import mascotas


def set_routers(app):
    app.include_router(
        router=sesiones.router,
        # prefix="/usuarios",
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
