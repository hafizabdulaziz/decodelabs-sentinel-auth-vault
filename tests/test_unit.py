import pytest
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate

def test_password_hashing():
    password = "SuperStrongPassword123!"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_user_schema_validation():
    user_data = {"email": "user@example.com", "password": "StrongPassword1!"}
    user = UserCreate(**user_data)
    assert user.email == "user@example.com"
    
    with pytest.raises(Exception):
        UserCreate(email="invalid-email", password="123")
