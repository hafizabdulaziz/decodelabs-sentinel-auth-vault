import pytest
import pytest_asyncio
import os
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch
from app.api.deps import get_db
from app.models.user import User
from app.core.security import get_password_hash
from datetime import datetime, timezone
import uuid

# Set env var before importing app to override the DB URL
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.main import app

@pytest.fixture(autouse=True)
def mock_rate_limiter():
    with patch("app.services.rate_limiter.RateLimiter.is_allowed", return_value=True):
        yield

@pytest_asyncio.fixture(scope="function")
async def db_session():
    # Mocking the session
    mock_session = AsyncMock()
    
    # Create a mock user
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
    
    user_query_count = [0]
    async def mock_execute(statement, *args, **kwargs):
        stmt_str = str(statement)
        res = MagicMock()
        if "mfa" in stmt_str.lower():
            res.scalars().first.return_value = None
        elif "role" in stmt_str.lower():
            res.scalars().all.return_value = []
        elif "users" in stmt_str.lower() or "user" in stmt_str.lower():
            user_query_count[0] += 1
            if user_query_count[0] == 1:
                res.scalars().first.return_value = None
            else:
                res.scalars().first.return_value = mock_user
        else:
            res.scalars().first.return_value = None
        return res

    mock_session.execute = AsyncMock(side_effect=mock_execute)
    mock_session.commit = AsyncMock()
    mock_session.add = MagicMock()
    
    return mock_session

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def _get_test_db():
        yield db_session
    
    app.dependency_overrides[get_db] = _get_test_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()
