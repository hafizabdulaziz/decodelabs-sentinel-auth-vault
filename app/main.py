from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from scalar_fastapi import get_scalar_api_reference

from app.api.v1.endpoints import (
    admin,
    agent,
    audit,
    auth,
    auth_refresh,
    health,
    metrics,
    mfa,
    users,
)
from app.core.security_headers import SecurityHeadersMiddleware

app = FastAPI(
    title="Sentinel Auth Vault API",
    version="1.0.0",
    description="""
# Sentinel Auth Vault API

Enterprise-Grade Zero Trust Authentication & Autonomous Security Engine.

## Features
- **Security:** Argon2id hashing, JWT, MFA.
- **Access Control:** RBAC & Fine-grained permissions.
- **Monitoring:** Observability, Audit Logs, IDS.
- **Operations:** Sliding-window Rate Limiting & Account Lockout.
""",
    contact={
        "name": "Sentinel Auth Vault Team",
        "url": "https://github.com/your-repo/sentinel-auth-vault",
    },
)

# ... (Middleware and Routers remain unchanged) ...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth_refresh.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(metrics.router, prefix="/api/v1", tags=["metrics"])
app.include_router(mfa.router, prefix="/api/v1/mfa", tags=["mfa"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(agent.router, prefix="/api/v1/agent", tags=["agent"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["audit"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sentinel Auth Vault API",
        version="1.0.0",
        description="Official API Documentation for Sentinel Auth Vault.",
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
        servers=[{"url": "http://localhost:8000"}],
    )
