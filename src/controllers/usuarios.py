class Usuario:
    pass


async def obtener_todos():
    return []


async def obtener_por_id(id: int):
    return None


async def obtener_por_email(email: str):
    return None


async def validar_credenciales(email: str, password: str) -> Usuario:
    if email != "rodri@casas.com":
        raise Exception("Usuario inexistente.")

    if password != "adrianrodrigocasas":
        raise Exception("Contraseña incorrecta.")

    usuario = Usuario()
    return usuario


async def create(usuario: Usuario):
    return usuario


async def update(usuario: Usuario):
    return usuario


async def delete(id: int):
    return True
