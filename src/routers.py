from entidades.usuarios.router import router as usuarios_router
from entidades.sesiones.router import router as sesiones_router
from entidades.auditorias.router import router as auditorias_router
from entidades.revisiones.router import router as revisiones_router
from entidades.relevamientos.router import router as relevamientos_router
from entidades.documentos.router import router as documentos_router
from entidades.objetivos_control.router import router as objetivos_control_router
from entidades.riesgos.router import router as riesgos_router
from entidades.controles.router import router as controles_router
from entidades.pruebas.router import router as pruebas_router
from entidades.links.router import router as relaciones_router
from entidades.observaciones.router import router as observaciones_router
from entidades.pedidos.router import router as pedidos_router
from entidades.archivos.router import router as archivos_router
from entidades.normativas.router import router as normativas_router
from entidades.aplicaciones.router import router as aplicaciones_router


def set_routers(app):
    app.include_router(
        router=usuarios_router,
        prefix="/api/v1/usuarios",
        tags=["Usuarios"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=sesiones_router,
        prefix="/api/v1/sesiones",
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

    app.include_router(
        router=controles_router,
        prefix="/api/v1/controles",
        tags=["Controles"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=pruebas_router,
        prefix="/api/v1/pruebas",
        tags=["Pruebas"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=relaciones_router,
        prefix="/api/v1/links",
        tags=["Links"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=observaciones_router,
        prefix="/api/v1/observaciones",
        tags=["Observaciones"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=pedidos_router,
        prefix="/api/v1/pedidos",
        tags=["Pedidos"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=archivos_router,
        prefix="/api/v1/archivos",
        tags=["Archivos"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=normativas_router,
        prefix="/api/v1/normativas",
        tags=["Normativas"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )

    app.include_router(
        router=aplicaciones_router,
        prefix="/api/v1/aplicaciones",
        tags=["Aplicaciones"],
        #####
        # dependencies=[Depends(get_token_header)],
        # responses={418: {"description": "I'm a teapot"}},
    )
