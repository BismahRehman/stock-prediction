
from datetime import timedelta, datetime

from jose import JWTError, jwt
from app.config import settings

from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================== PASSWORD HELPERS =========================================

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]       # take only first 72 bytes
    safe_password = password_bytes.decode("utf-8", "ignore")  # safely drop incomplete characters
    return password_context.hash(safe_password)

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire_time})
    encode_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encode_jwt


def verify_access_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None
