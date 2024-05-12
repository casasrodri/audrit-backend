from datetime import datetime, timedelta, UTC

from jose import JWTError, jwt

from dotenv import load_dotenv

load_dotenv()
import os

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES"))


async def crear_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    # ya = datetime.utcnow()
    ya = datetime.now(UTC)

    if expires_delta:
        expire = ya + expires_delta
    else:
        expire = ya + timedelta(minutes=JWT_EXPIRE_MINUTES)

    to_encode.update({"iat": ya, "exp": expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt


async def leer_token(jwt_token: str) -> str | JWTError:
    """Recibe un token y devuelve el email del usuario que lo generó"""
    payload = jwt.decode(
        token=jwt_token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
    )

    email: str = payload.get("sub")
    return email
