import pytest
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.core.config import settings

def test_create_and_verify_access_token():
    subject = "user@example.com"
    token = create_access_token(subject)
    decoded = verify_token(token)
    assert decoded is not None
    assert decoded["sub"] == subject
    assert decoded["type"] == "access"

def test_create_and_verify_refresh_token():
    subject = "user@example.com"
    token = create_refresh_token(subject)
    decoded = verify_token(token)
    assert decoded is not None
    assert decoded["sub"] == subject
    assert decoded["type"] == "refresh"

def test_verify_tampered_token():
    token = create_access_token("user@example.com")
    tampered_token = token[:-5] + "aaaaa"
    decoded = verify_token(tampered_token)
    assert decoded is None
