from datetime import timedelta, datetime
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings


# -----------------------------------------
# Password hashing context (bcrypt)
# -----------------------------------------
password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================================
# PASSWORD UTILITIES
# =========================================

# Hash password before storing in DB
def hash_password(password: str) -> str:

    # ⚠️ You truncate password to 72 bytes (bcrypt limit handling)
    password_bytes = password.encode("utf-8")[:72]

    # Safe decode (drops invalid trailing bytes)
    safe_password = password_bytes.decode("utf-8", "ignore")

    return password_context.hash(safe_password)


# Verify plain password against hashed password
def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


# =========================================
# JWT TOKEN CREATION
# =========================================
def create_access_token(data: dict):

    to_encode = data.copy()

    # Token expiry (15 min access token)
    expire_time = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire_time})

    # Encode JWT
    encode_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encode_jwt


# =========================================
# JWT VALIDATION
# =========================================
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