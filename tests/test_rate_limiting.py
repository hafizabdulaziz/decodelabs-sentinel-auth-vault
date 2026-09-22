import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_rate_limiting_exceeded():
    # Mock RateLimiter to return False (limit exceeded)
    with patch("app.services.rate_limiter.RateLimiter.is_allowed", return_value=False):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            # We need an endpoint that uses RateLimitChecker. 
            # For testing, let's assume we applied it to /api/v1/auth/login
            response = await ac.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "Password123!"})
            assert response.status_code == 429
