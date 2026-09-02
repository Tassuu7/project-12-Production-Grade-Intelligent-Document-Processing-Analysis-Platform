"""Unit tests for cryptographic password hashing and tokens."""
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    calculate_file_hash,
    sanitize_filename
)

def test_password_hashing_and_verification():
    raw_pwd = "SecurePassword@2026!"
    hashed = hash_password(raw_pwd)
    assert hashed.startswith("pbkdf2_sha256$")
    assert verify_password(raw_pwd, hashed) is True
    assert verify_password("WrongPassword123", hashed) is False

def test_jwt_token_generation_and_decoding():
    token = create_access_token(subject=42, role="admin", email="admin@example.com")
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "42"
    assert payload["role"] == "admin"
    assert payload["email"] == "admin@example.com"
    assert payload["type"] == "access"

def test_filename_sanitization():
    unsafe = "../../../etc/passwd.pdf"
    safe = sanitize_filename(unsafe)
    assert "/" not in safe
    assert ".." not in safe
    assert safe.endswith(".pdf")
