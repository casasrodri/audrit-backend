from entidades.usuarios.model import UsuarioAutenticacion


class DatabaseMock:
    def __init__(self) -> None:
        pass

    def obtener_usuario_por_email(self, email: str):
        if email == "rodri@casas.com":
            return UsuarioAutenticacion(
                nombre="Rodrigoooo",
                apellido="Casas",
                email="rodri@casas.com",
                password="0fd98s9f08s0d9f8ks0d98fks0fd9s0dl9f",
            )

        return None
