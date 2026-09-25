import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_read_users_me_unauthenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/users/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_read_users_me_authenticated():
    from app.api.deps import get_db, get_current_user
    from app.models.user import User
    from app.core.security import create_access_token, get_password_hash
    import uuid
    from datetime import datetime, timezone

    mock_session = AsyncMock()
    now = datetime.now(timezone.utc)
    mock_user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        hashed_password=get_password_hash("StrongPassword1!"),
        is_active=True,
        is_superuser=False,
        created_at=now,
        updated_at=now
    )
    mock_result = MagicMock()
    mock_result.scalars().first.return_value = mock_user
    mock_session.execute.return_value = mock_result

    async def _get_test_db():
        yield mock_session

    app.dependency_overrides[get_db] = _get_test_db

    token = create_access_token("test@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/users/me", headers=headers)
    
    app.dependency_overrides.clear()
    assert response.status_code == 200
