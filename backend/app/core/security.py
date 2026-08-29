import base64
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def create_access_token(
    subject: Union[str, int],
    role: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": int(expire.timestamp()),
        "sub": str(subject),
        "role": role,
        "iat": int(datetime.now(timezone.utc).timestamp())
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def encrypt_sensitive_string(plain_text: str) -> str:
    """Simple obfuscation/encryption helper for storing connection credentials safely."""
    encoded_bytes = base64.b64encode(plain_text.encode("utf-8"))
    return encoded_bytes.decode("utf-8")


def decrypt_sensitive_string(cipher_text: str) -> str:
    """Decrypt obfuscated connection strings."""
    try:
        decoded_bytes = base64.b64decode(cipher_text.encode("utf-8"))
        return decoded_bytes.decode("utf-8")
    except Exception:
        return cipher_text
