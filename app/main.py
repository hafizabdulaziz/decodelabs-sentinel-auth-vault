from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from scalar_fastapi import get_scalar_api_reference
from app.api.v1.endpoints import auth, users, auth_refresh, health, metrics

app = FastAPI(
    title="Sentinel Auth Vault",
    version="0.1.0",
    description="Enterprise-Grade Zero Trust Authentication & Autonomous Security Engine",
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth_refresh.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(metrics.router, prefix="/api/v1", tags=["metrics"])

# ... custom_openapi and scalar_html unchanged ...

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sentinel Auth Vault API",
        version="0.1.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Sentinel Auth Vault API",
    )
