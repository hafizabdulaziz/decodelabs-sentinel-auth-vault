import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_rate_limiting_exceeded(client: AsyncClient):
    # Mock RateLimiter to return False (limit exceeded)
    with patch("app.services.rate_limiter.RateLimiter.is_allowed", return_value=False):
        response = await client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "Password123!"})
        assert response.status_code == 429
