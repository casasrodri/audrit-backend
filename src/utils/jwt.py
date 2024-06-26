from datetime import UTC, datetime, timedelta

from config.env import JWT
from jose import JWTError, jwt


async def crear_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    ya = datetime.now(UTC)

    if expires_delta:
        expire = ya + expires_delta
    else:
        expire = ya + timedelta(minutes=JWT.EXPIRE_MINUTES)

    to_encode.update({"iat": ya, "exp": expire})

    encoded_jwt = jwt.encode(to_encode, JWT.SECRET_KEY, algorithm=JWT.ALGORITHM)

    return encoded_jwt


async def leer_token(jwt_token: str) -> str | JWTError:
    """Recibe un token y devuelve el email del usuario que lo generó"""
    payload = jwt.decode(
        token=jwt_token, key=JWT.SECRET_KEY, algorithms=[JWT.ALGORITHM]
    )

    email: str = payload.get("sub")
    return email
