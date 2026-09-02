"""
Cryptographic Security, Password Hashing, and JWT Authorization.
"""
import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union
import jwt
from app.core.config import settings

PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 100_000
SALT_BYTES = 16

def generate_salt() -> str:
    return secrets.token_hex(SALT_BYTES)

def hash_password(password: str, salt: Optional[str] = None) -> str:
    if not salt:
        salt = generate_salt()
    pwd_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    derived_key = hashlib.pbkdf2_hmac(PBKDF2_ALGORITHM, pwd_bytes, salt_bytes, PBKDF2_ITERATIONS, dklen=32)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt}${derived_key.hex()}"

def verify_password(plain_password: str, stored_hash: str) -> bool:
    try:
        parts = stored_hash.split("$")
        if len(parts) != 4:
            return False
        algo, iterations_str, salt, expected_hash = parts
        if algo != "pbkdf2_sha256":
            return False
        iterations = int(iterations_str)
        pwd_bytes = plain_password.encode("utf-8")
        salt_bytes = salt.encode("utf-8")
        derived_key = hashlib.pbkdf2_hmac(PBKDF2_ALGORITHM, pwd_bytes, salt_bytes, iterations, dklen=32)
        return hmac.compare_digest(derived_key.hex(), expected_hash)
    except Exception:
        return False

def create_access_token(subject: Union[str, int], role: str, email: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: Dict[str, Any] = {
        "sub": str(subject),
        "role": role,
        "email": email,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(subject: Union[str, int], role: str, email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload: Dict[str, Any] = {
        "sub": str(subject),
        "role": role,
        "email": email,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        return None

def calculate_file_hash(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def sanitize_filename(filename: str) -> str:
    import re
    base = os.path.basename(filename)
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', base)
    sanitized = re.sub(r'_+', '_', sanitized)
    if not sanitized or sanitized.startswith('.'):
        sanitized = f"doc_{secrets.token_hex(4)}{os.path.splitext(filename)[1]}"
    return sanitized
