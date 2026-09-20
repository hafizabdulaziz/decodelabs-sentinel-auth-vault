from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from scalar_fastapi import get_scalar_api_reference
from app.api.v1.endpoints import auth, users, auth_refresh

app = FastAPI(title="Sentinel Auth Vault", version="0.1.0")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth_refresh.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Sentinel Auth Vault API",
    )
