import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_auth_flow_e2e(client: AsyncClient):
    # 1. Register
    user_data = {"email": "test@example.com", "password": "StrongPassword1!"}
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201

    # 2. Login
    response = await client.post("/api/v1/auth/login", json=user_data)
    assert response.status_code == 200
    data = response.json()["data"]
    access_token = data["access_token"]

    # 3. Access Protected Route
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
