from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sentinel Auth Vault - Enterprise Security Engine</title>
        <style>
            body { background-color: #0f172a; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .card { background: #1e293b; padding: 2.5rem; border-radius: 1rem; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); max-width: 600px; width: 100%; border: 1px solid #334155; }
            h1 { color: #38bdf8; margin-top: 0; font-size: 1.8rem; }
            p { color: #94a3b8; line-height: 1.6; }
            .links { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 2rem; }
            a { background: #0284c7; color: white; padding: 0.75rem 1rem; border-radius: 0.5rem; text-decoration: none; text-align: center; font-weight: 500; transition: background 0.2s; }
            a:hover { background: #0369a1; }
            .badge { display: inline-block; background: #22c55e; color: #052e16; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.85rem; font-weight: 600; margin-bottom: 1rem; }
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">System Online & Secure</span>
            <h1>Sentinel Auth Vault</h1>
            <p>Enterprise-Grade Zero Trust Authentication & Autonomous Security Engine. All security services, APIs, metrics, and health diagnostics are unified under this instance.</p>
            <div class="links">
                <a href="/scalar" target="_blank">📚 API Docs (Scalar)</a>
                <a href="/api/v1/health" target="_blank">🩺 System Health</a>
                <a href="/api/v1/metrics" target="_blank">📊 Prometheus Metrics</a>
                <a href="/openapi.json" target="_blank">📄 OpenAPI Spec</a>
            </div>
        </div>
    </body>
    </html>
    """
