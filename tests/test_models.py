import uuid
from datetime import datetime, timezone

from app.models.audit import AuditLog
from app.models.mfa import MFAModel
from app.models.role import Role
from app.models.user import User


def test_user_model():
    now = datetime.now(timezone.utc)
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        email="test@example.com",
        hashed_password="hash",
        is_active=True,
        is_superuser=False,
        created_at=now,
        updated_at=now
    )
    assert user.id == user_id
    assert user.email == "test@example.com"
    assert user.is_active is True

def test_role_model():
    role_id = uuid.uuid4()
    role = Role(id=role_id, name="admin")
    assert role.id == role_id
    assert role.name == "admin"

def test_mfa_model():
    mfa = MFAModel(id=uuid.uuid4(), user_id=uuid.uuid4(), secret="secret", is_enabled=True)
    assert mfa.is_enabled is True
    assert mfa.secret == "secret"

def test_audit_model():
    now = datetime.now(timezone.utc)
    audit = AuditLog(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        action="login",
        resource="auth",
        payload={},
        ip_address="127.0.0.1",
        severity="INFO",
        created_at=now
    )
    assert audit.action == "login"
    assert audit.created_at == now
