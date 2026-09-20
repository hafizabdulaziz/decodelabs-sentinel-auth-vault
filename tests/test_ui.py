import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_scalar_ui_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/scalar")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
