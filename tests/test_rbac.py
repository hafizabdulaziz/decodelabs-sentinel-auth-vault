import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_admin_access_forbidden():
    # Mock RoleChecker to fail
    with patch("app.api.deps.RoleChecker.__call__", side_effect=Exception("Forbidden")):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/admin/admin-only")
            assert response.status_code != 200
