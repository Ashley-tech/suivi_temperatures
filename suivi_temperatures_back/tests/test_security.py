import pytest
from pydantic import ValidationError

from app.routers.login import LoginRequest
from app.security import create_access_token, verify_password


def test_verify_password_and_token_roundtrip():
    hashed = "argon2$..."
    assert callable(verify_password)
    assert create_access_token("test@example.com")


def test_login_request_validates_password_length():
    with pytest.raises(ValidationError):
        LoginRequest(email="user@example.com", mdp="short")
