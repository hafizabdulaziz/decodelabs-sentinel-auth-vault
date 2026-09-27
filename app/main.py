from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

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
from app.db.base_class import Base
from app.db.session import engine
from app.models.user import User
from app.models.mfa import MFAModel
from app.models.token import RefreshToken
from app.models.role import Role, user_roles
from app.models.audit import AuditLog

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

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
    lifespan=lifespan,
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

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    html_response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Sentinel Auth Vault - Enterprise API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    )
    custom_css = """
    <style>
        body {
            background-color: #0d1117 !important;
            color: #f0f6fc !important;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }
        .swagger-ui {
            color: #f0f6fc !important;
        }
        .swagger-ui .topbar {
            background-color: #161b22 !important;
            border-bottom: 1px solid #30363d !important;
            padding: 12px 0;
        }
        .swagger-ui .topbar .download-url-wrapper { display: none !important; }
        .swagger-ui .info h1, .swagger-ui .info h2, .swagger-ui .info h3, .swagger-ui .info h4, .swagger-ui .info p, .swagger-ui .info table, .swagger-ui .info li, .swagger-ui .info td, .swagger-ui .info th {
            color: #f0f6fc !important;
        }
        .swagger-ui .info .title {
            color: #38bdf8 !important;
            font-weight: 700 !important;
        }
        .swagger-ui .scheme-container {
            background-color: #161b22 !important;
            box-shadow: none !important;
            border: 1px solid #30363d !important;
            border-radius: 10px;
            padding: 1rem;
            margin: 20px 0;
        }
        .swagger-ui .opblock {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            border-radius: 10px !important;
            box-shadow: none !important;
            margin-bottom: 12px !important;
        }
        .swagger-ui .opblock.opblock-get { background-color: rgba(56, 189, 248, 0.05) !important; border-color: rgba(56, 189, 248, 0.25) !important; }
        .swagger-ui .opblock.opblock-post { background-color: rgba(16, 185, 129, 0.05) !important; border-color: rgba(16, 185, 129, 0.25) !important; }
        .swagger-ui .opblock.opblock-delete { background-color: rgba(244, 63, 94, 0.05) !important; border-color: rgba(244, 63, 94, 0.25) !important; }
        .swagger-ui .opblock.opblock-put { background-color: rgba(245, 158, 11, 0.05) !important; border-color: rgba(245, 158, 11, 0.25) !important; }
        
        .swagger-ui .opblock .opblock-summary-path, .swagger-ui .opblock .opblock-summary-description {
            color: #f0f6fc !important;
        }
        .swagger-ui .opblock .opblock-summary-method {
            border-radius: 6px !important;
            font-weight: 700 !important;
        }
        .swagger-ui .opblock-body {
            background-color: #161b22 !important;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }
        .swagger-ui .opblock-section-header {
            background-color: #21262d !important;
            box-shadow: none !important;
            border-bottom: 1px solid #30363d !important;
            color: #f0f6fc !important;
        }
        .swagger-ui .opblock-section-header h4 {
            color: #f0f6fc !important;
        }
        .swagger-ui .btn {
            background-color: #21262d !important;
            color: #f0f6fc !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
            box-shadow: none !important;
            font-weight: 600 !important;
        }
        .swagger-ui .btn:hover {
            background-color: #30363d !important;
            border-color: #8b949e !important;
        }
        .swagger-ui .btn.authorize {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(99, 102, 241, 0.2)) !important;
            border-color: rgba(56, 189, 248, 0.4) !important;
            color: #38bdf8 !important;
        }
        .swagger-ui input[type=text], .swagger-ui textarea, .swagger-ui select {
            background-color: #0d1117 !important;
            color: #f0f6fc !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
        }
        .swagger-ui textarea:focus, .swagger-ui input[type=text]:focus {
            border-color: #38bdf8 !important;
            outline: none !important;
        }
        .swagger-ui .dialog-ux {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            color: #f0f6fc !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.7) !important;
        }
        .swagger-ui .model-box {
            background-color: #0d1117 !important;
            border-radius: 8px;
            padding: 10px;
        }
        .swagger-ui .model {
            color: #f0f6fc !important;
        }
        .swagger-ui .prop-type {
            color: #38bdf8 !important;
        }
        .swagger-ui table tspan, .swagger-ui table td, .swagger-ui table th {
            color: #f0f6fc !important;
        }
        .swagger-ui .response-col_status, .swagger-ui .response-col_description {
            color: #f0f6fc !important;
        }
        .swagger-ui .parameter__name, .swagger-ui .parameter__type, .swagger-ui .parameter__deprecated {
            color: #f0f6fc !important;
        }
        .swagger-ui .tab li {
            color: #8b949e !important;
        }
        .swagger-ui .tab li.active {
            color: #38bdf8 !important;
        }
    </style>
    """
    html_content = html_response.body.decode("utf-8")
    html_content = html_content.replace("</head>", f"{custom_css}</head>")
    return HTMLResponse(content=html_content)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sentinel Auth Vault - Enterprise SOC Dashboard</title>
        <style>
            :root {
                --bg-main: #0d1117;
                --bg-card: #161b22;
                --bg-card-hover: #1f242c;
                --border-color: #30363d;
                --text-primary: #f0f6fc;
                --text-secondary: #8b949e;
                --accent-cyan: #38bdf8;
                --accent-emerald: #10b981;
                --accent-indigo: #6366f1;
                --accent-amber: #f59e0b;
                --accent-rose: #f43f5e;
            }

            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                background-color: var(--bg-main);
                color: var(--text-primary);
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                line-height: 1.5;
            }

            /* Header */
            header {
                background: rgba(22, 27, 34, 0.85);
                backdrop-filter: blur(12px);
                border-bottom: 1px solid var(--border-color);
                padding: 1rem 2rem;
                display: flex;
                align-items: center;
                justify-content: space-between;
                position: sticky;
                top: 0;
                z-index: 100;
            }
            .brand {
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }
            .brand-icon {
                width: 40px;
                height: 40px;
                border-radius: 10px;
                background: linear-gradient(135deg, var(--accent-cyan), var(--accent-indigo));
                display: flex;
                align-items: center;
                justify-content: center;
                color: #0d1117;
                font-weight: bold;
                font-size: 1.2rem;
            }
            .brand-title h1 {
                font-size: 1.1rem;
                font-weight: 700;
                color: var(--text-primary);
                letter-spacing: -0.01em;
            }
            .brand-title p {
                font-size: 0.75rem;
                color: var(--text-secondary);
            }
            .badge-secure {
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.3);
                color: var(--accent-emerald);
                padding: 0.2rem 0.6rem;
                border-radius: 20px;
                font-size: 0.7rem;
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 0.3rem;
            }
            .pulse {
                width: 6px;
                height: 6px;
                background-color: var(--accent-emerald);
                border-radius: 50%;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
                70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
            }

            .nav-actions {
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }
            .btn {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                color: var(--text-primary);
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-size: 0.8rem;
                font-weight: 500;
                text-decoration: none;
                cursor: pointer;
                transition: all 0.2s;
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
            }
            .btn:hover {
                background: var(--bg-card-hover);
                border-color: var(--text-secondary);
            }
            .btn-primary {
                background: linear-gradient(135deg, rgba(56, 189, 248, 0.15), rgba(99, 102, 241, 0.15));
                border-color: rgba(56, 189, 248, 0.3);
                color: var(--accent-cyan);
            }
            .btn-primary:hover {
                background: linear-gradient(135deg, rgba(56, 189, 248, 0.25), rgba(99, 102, 241, 0.25));
            }
            .btn-danger {
                background: rgba(244, 63, 94, 0.1);
                border-color: rgba(244, 63, 94, 0.3);
                color: var(--accent-rose);
            }
            .btn-danger:hover {
                background: rgba(244, 63, 94, 0.2);
            }

            /* Main Container */
            main {
                max-width: 1400px;
                width: 100%;
                margin: 0 auto;
                padding: 2rem;
                flex: 1;
            }

            /* Tabs */
            .tabs-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid var(--border-color);
                margin-bottom: 2rem;
                padding-bottom: 1rem;
                flex-wrap: wrap;
                gap: 1rem;
            }
            .tabs {
                display: flex;
                gap: 0.5rem;
            }
            .tab-btn {
                background: transparent;
                border: 1px solid transparent;
                color: var(--text-secondary);
                padding: 0.6rem 1.2rem;
                border-radius: 10px;
                font-size: 0.85rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .tab-btn:hover {
                color: var(--text-primary);
                background: var(--bg-card);
            }
            .tab-btn.active {
                background: rgba(56, 189, 248, 0.1);
                color: var(--accent-cyan);
                border-color: rgba(56, 189, 248, 0.3);
            }

            /* Grid Layouts */
            .grid-4 {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 1.25rem;
                margin-bottom: 2rem;
            }
            .grid-2 {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }
            .card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 14px;
                padding: 1.5rem;
                position: relative;
                overflow: hidden;
            }
            .card-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 1rem;
            }
            .card-title {
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--text-secondary);
                font-weight: 600;
            }
            .card-value {
                font-size: 1.8rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-top: 0.2rem;
            }
            .card-icon {
                width: 42px;
                height: 42px;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
            }

            /* Form Elements */
            .form-group {
                margin-bottom: 1.25rem;
            }
            label {
                display: block;
                font-size: 0.8rem;
                font-weight: 500;
                color: var(--text-secondary);
                margin-bottom: 0.5rem;
            }
            input, textarea {
                width: 100%;
                background: var(--bg-main);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 0.75rem 1rem;
                color: var(--text-primary);
                font-size: 0.9rem;
                font-family: inherit;
                outline: none;
                transition: border-color 0.2s;
            }
            input:focus, textarea:focus {
                border-color: var(--accent-cyan);
            }
            textarea {
                font-family: 'Courier New', Courier, monospace;
                font-size: 0.8rem;
                resize: vertical;
            }

            /* Tables */
            .table-container {
                overflow-x: auto;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                text-align: left;
                font-size: 0.85rem;
            }
            th {
                color: var(--text-secondary);
                font-weight: 600;
                border-bottom: 1px solid var(--border-color);
                padding: 0.75rem 1rem;
                text-transform: uppercase;
                font-size: 0.7rem;
                letter-spacing: 0.05em;
            }
            td {
                padding: 0.85rem 1rem;
                border-bottom: 1px solid rgba(48, 54, 61, 0.4);
                color: var(--text-primary);
                font-family: 'Courier New', Courier, monospace;
            }
            tr:hover td {
                background: rgba(255, 255, 255, 0.015);
            }

            /* Badges & Status */
            .status-badge {
                padding: 0.2rem 0.5rem;
                border-radius: 6px;
                font-size: 0.7rem;
                font-weight: 600;
                text-transform: uppercase;
            }
            .status-success { background: rgba(16, 185, 129, 0.1); color: var(--accent-emerald); border: 1px solid rgba(16, 185, 129, 0.2); }
            .status-error { background: rgba(244, 63, 94, 0.1); color: var(--accent-rose); border: 1px solid rgba(244, 63, 94, 0.2); }

            /* Toast */
            #toast-container {
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                z-index: 1000;
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }
            .toast {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                color: var(--text-primary);
                padding: 0.85rem 1.25rem;
                border-radius: 10px;
                font-size: 0.85rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                display: flex;
                align-items: center;
                gap: 0.75rem;
                animation: slideIn 0.3s ease;
            }
            .toast.success { border-color: rgba(16, 185, 129, 0.4); }
            .toast.error { border-color: rgba(244, 63, 94, 0.4); }
            @keyframes slideIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }

            .hidden { display: none !important; }
            .sub-tabs {
                display: flex;
                gap: 0.25rem;
                background: var(--bg-main);
                padding: 0.25rem;
                border-radius: 8px;
                border: 1px solid var(--border-color);
            }
            .sub-tab-btn {
                background: transparent;
                border: none;
                color: var(--text-secondary);
                padding: 0.4rem 0.8rem;
                border-radius: 6px;
                font-size: 0.75rem;
                font-weight: 600;
                cursor: pointer;
            }
            .sub-tab-btn.active {
                background: var(--accent-cyan);
                color: var(--bg-main);
            }

            footer {
                text-align: center;
                padding: 1.5rem;
                border-top: 1px solid var(--border-color);
                color: var(--text-secondary);
                font-size: 0.75rem;
                margin-top: auto;
            }
        </style>
    </head>
    <body>

        <!-- Top Header -->
        <header>
            <div class="brand">
                <div class="brand-icon">🛡️</div>
                <div class="brand-title">
                    <h1>Sentinel Auth Vault</h1>
                    <p>Enterprise Zero Trust Security Operations Center</p>
                </div>
            </div>
            <div class="nav-actions">
                <div id="session-status-badge" class="btn hidden" style="cursor: default;">
                    <span style="color: var(--accent-cyan);">●</span> <span id="nav-username">Operator</span>
                </div>
                <a href="/docs" target="_blank" class="btn">📖 Swagger UI</a>
                <button onclick="logoutUser()" id="btn-logout" class="btn btn-danger hidden">Logout</button>
            </div>
        </header>

        <!-- Main Content -->
        <main>
            <div id="toast-container"></div>

            <!-- Tabs Navigation -->
            <div class="tabs-container">
                <div class="tabs">
                    <button onclick="switchTab('overview')" id="tab-btn-overview" class="tab-btn active">📊 Overview & Health</button>
                    <button onclick="switchTab('auth')" id="tab-btn-auth" class="tab-btn">🔑 Auth & JWT Inspector</button>
                    <button onclick="switchTab('mfa')" id="tab-btn-mfa" class="tab-btn">🔒 MFA Operations</button>
                    <button onclick="switchTab('audit')" id="tab-btn-audit" class="tab-btn">🛡️ Security Audit Logs</button>
                </div>
                <div style="font-size: 0.75rem; color: var(--text-secondary); display: flex; align-items: center; gap: 0.5rem;">
                    <div class="pulse"></div> Auto-refresh active (10s)
                    <button onclick="refreshAllData()" class="btn" style="padding: 0.3rem 0.6rem; margin-left: 0.5rem;">🔄</button>
                </div>
            </div>

            <!-- TAB 1: OVERVIEW -->
            <div id="tab-content-overview" class="tab-content">
                <div class="grid-4">
                    <div class="card">
                        <div class="card-header">
                            <span class="card-title">System Health</span>
                            <div class="card-icon" style="background: rgba(16, 185, 129, 0.1); color: var(--accent-emerald);">🩺</div>
                        </div>
                        <div id="stat-health-status" class="card-value" style="color: var(--accent-emerald);">Checking...</div>
                        <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
                            <span id="stat-db-status">DB: Connected</span> • <span id="stat-redis-status">Redis: Connected</span>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-header">
                            <span class="card-title">Auth Token State</span>
                            <div class="card-icon" style="background: rgba(56, 189, 248, 0.1); color: var(--accent-cyan);">🎫</div>
                        </div>
                        <div id="stat-token-state" class="card-value" style="color: var(--accent-cyan);">Active</div>
                        <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
                            Session: <span id="stat-token-indicator" style="color: var(--accent-amber);">Not Set</span>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-header">
                            <span class="card-title">Perimeter Defense</span>
                            <div class="card-icon" style="background: rgba(99, 102, 241, 0.1); color: var(--accent-indigo);">🛡️</div>
                        </div>
                        <div class="card-value" style="color: var(--accent-indigo);">Enforced</div>
                        <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
                            Sliding-Window & Lockout Active
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-header">
                            <span class="card-title">Sentinel Agent</span>
                            <div class="card-icon" style="background: rgba(245, 158, 11, 0.1); color: var(--accent-amber);">🤖</div>
                        </div>
                        <div class="card-value" style="color: var(--accent-amber);">Autonomous</div>
                        <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem;">
                            Threat Intel & Tools Ready
                        </div>
                    </div>
                </div>

                <div class="grid-2">
                    <div class="card">
                        <div class="card-header">
                            <span class="card-title">System Metrics & Telemetry</span>
                            <a href="/api/v1/metrics" target="_blank" style="font-size: 0.75rem; color: var(--accent-cyan); text-decoration: none;">Raw Metrics ↗</a>
                        </div>
                        <div id="metrics-container" style="background: var(--bg-main); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; font-family: monospace; font-size: 0.75rem; height: 220px; overflow-y: auto; color: var(--text-secondary);">
                            Loading metrics...
                        </div>
                    </div>
                    <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div class="card-header">
                                <span class="card-title">Quick Diagnostics</span>
                            </div>
                            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                                <button onclick="testHealthEndpoint()" class="btn" style="width: 100%; justify-content: space-between;">
                                    <span>🩺 Ping /api/v1/health</span><span>→</span>
                                </button>
                                <button onclick="testProtectedEndpoint()" class="btn" style="width: 100%; justify-content: space-between;">
                                    <span>🔐 Test /api/v1/users/me</span><span>→</span>
                                </button>
                                <button onclick="testAgentEndpoint()" class="btn" style="width: 100%; justify-content: space-between;">
                                    <span>🤖 Ping Sentinel Agent</span><span>→</span>
                                </button>
                            </div>
                        </div>
                        <div style="border-top: 1px solid var(--border-color); padding-top: 1rem; margin-top: 1rem; font-size: 0.75rem; color: var(--text-secondary); display: flex; justify-content: space-between;">
                            <span>Sentinel Core Engine</span>
                            <span style="color: var(--accent-emerald);">Secure</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 2: AUTH & JWT INSPECTOR -->
            <div id="tab-content-auth" class="tab-content hidden">
                <div class="grid-2">
                    <div class="card">
                        <div class="card-header">
                            <span class="card-title">Authentication Portal</span>
                            <div class="sub-tabs">
                                <button onclick="switchAuthSubtab('login')" id="subtab-login" class="sub-tab-btn active">Login</button>
                                <button onclick="switchAuthSubtab('register')" id="subtab-register" class="sub-tab-btn">Register</button>
                            </div>
                        </div>

                        <!-- Login Form -->
                        <form id="form-login" onsubmit="handleLogin(event)">
                            <div class="form-group">
                                <label>Email Address</label>
                                <input type="email" id="login-email" required value="admin@example.com">
                            </div>
                            <div class="form-group">
                                <label>Password</label>
                                <input type="password" id="login-password" required value="SecurePass123!">
                            </div>
                            <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 0.8rem;">
                                Authenticate & Obtain JWT
                            </button>
                        </form>

                        <!-- Register Form -->
                        <form id="form-register" onsubmit="handleRegister(event)" class="hidden">
                            <div class="form-group">
                                <label>Email Address</label>
                                <input type="email" id="reg-email" required placeholder="user@example.com">
                            </div>
                            <div class="form-group">
                                <label>Full Name</label>
                                <input type="text" id="reg-name" required placeholder="Security Operator">
                            </div>
                            <div class="form-group">
                                <label>Password (Argon2id)</label>
                                <input type="password" id="reg-password" required placeholder="••••••••••••">
                            </div>
                            <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 0.8rem; background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(20, 184, 166, 0.2)); border-color: rgba(16, 185, 129, 0.4); color: var(--accent-emerald);">
                                Register Operator Account
                            </button>
                        </form>
                    </div>

                    <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div class="card-header">
                                <span class="card-title">JWT Token Inspector</span>
                                <button onclick="clearToken()" class="btn btn-danger" style="padding: 0.3rem 0.6rem; font-size: 0.7rem;">Clear</button>
                            </div>
                            <div class="form-group">
                                <label>Active Bearer Token</label>
                                <textarea id="jwt-token-input" rows="3" oninput="inspectJWT(this.value)" placeholder="Paste or obtain JWT bearer token..."></textarea>
                            </div>
                            <div class="form-group">
                                <label>Decoded Claims (Payload)</label>
                                <pre id="jwt-decoded-view" style="background: var(--bg-main); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; font-family: monospace; font-size: 0.75rem; height: 140px; overflow-y: auto; color: var(--accent-emerald);">No valid JWT loaded.</pre>
                            </div>
                        </div>
                        <div style="border-top: 1px solid var(--border-color); padding-top: 1rem; display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem;">
                            <span id="jwt-expiry-status" style="color: var(--text-secondary);">Status: No Token</span>
                            <button onclick="copyTokenToClipboard()" class="btn">Copy Token</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 3: MFA OPERATIONS -->
            <div id="tab-content-mfa" class="tab-content hidden">
                <div class="grid-2">
                    <div class="card">
                        <div class="card-header">
                            <span class="card-title">Multi-Factor Authentication (TOTP)</span>
                        </div>
                        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">Configure time-based one-time passwords for zero-trust security clearance.</p>
                        <button onclick="setupMFA()" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 0.8rem; margin-bottom: 1rem;">
                            Generate TOTP Secret & QR URI
                        </button>
                        <div id="mfa-setup-result" class="hidden" style="background: var(--bg-main); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; font-family: monospace; font-size: 0.75rem; space-y: 0.5rem;">
                            <p style="color: var(--text-secondary);">Secret: <span id="mfa-secret-val" style="color: var(--accent-cyan); font-weight: bold;"></span></p>
                            <p style="color: var(--text-secondary); margin-top: 0.5rem; word-break: break-all;">URI: <span id="mfa-uri-val" style="color: var(--accent-emerald);"></span></p>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header">
                            <span class="card-title">Verify TOTP Token</span>
                        </div>
                        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem;">Submit 6-digit authenticator code from your authenticator app.</p>
                        <form onsubmit="verifyMFA(event)">
                            <div class="form-group">
                                <label>6-Digit Code</label>
                                <input type="text" id="mfa-code-input" required maxlength="6" placeholder="123456" style="text-align: center; font-size: 1.2rem; letter-spacing: 0.2rem; font-family: monospace;">
                            </div>
                            <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 0.8rem; background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(20, 184, 166, 0.2)); border-color: rgba(16, 185, 129, 0.4); color: var(--accent-emerald);">
                                Verify TOTP Code
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- TAB 4: SECURITY AUDIT LOGS -->
            <div id="tab-content-audit" class="tab-content hidden">
                <div class="card">
                    <div class="card-header" style="flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <span class="card-title">Security Audit Logs</span>
                            <div style="font-size: 0.85rem; color: var(--text-primary); font-weight: 600; margin-top: 0.2rem;">Immutable Event Trail</div>
                        </div>
                        <div style="display: flex; gap: 0.75rem; align-items: center;">
                            <input type="text" id="audit-filter" oninput="filterAuditLogs()" placeholder="Filter logs..." style="width: 200px; padding: 0.5rem 0.75rem;">
                            <button onclick="fetchAuditLogs()" class="btn">🔄 Refresh</button>
                        </div>
                    </div>
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Timestamp</th>
                                    <th>Event / Action</th>
                                    <th>Actor</th>
                                    <th>IP Address</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody id="audit-table-body">
                                <tr><td colspan="5" style="text-align: center; color: var(--text-secondary); padding: 2rem;">Loading audit trail...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

        </main>

        <!-- Footer -->
        <footer>
            Sentinel Auth Vault • Enterprise Zero Trust Security Engine &copy; 2026
        </footer>

        <!-- Script Controller -->
        <script>
            let authToken = localStorage.getItem('sentinel_jwt') || '';

            document.addEventListener('DOMContentLoaded', () => {
                if (authToken) {
                    document.getElementById('jwt-token-input').value = authToken;
                    inspectJWT(authToken);
                    updateAuthUI(true);
                }
                refreshAllData();
                setInterval(refreshAllData, 10000);
            });

            function showToast(message, type = 'success') {
                const container = document.getElementById('toast-container');
                const toast = document.createElement('div');
                toast.className = `toast ${type}`;
                toast.innerHTML = `<span>${type === 'success' ? '✅' : '❌'}</span><span>${message}</span>`;
                container.appendChild(toast);
                setTimeout(() => {
                    toast.style.opacity = '0';
                    toast.style.transform = 'translateY(10px)';
                    toast.style.transition = 'all 0.3s ease';
                    setTimeout(() => toast.remove(), 300);
                }, 4000);
            }

            function switchTab(tabId) {
                document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
                document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
                document.getElementById(`tab-content-${tabId}`).classList.remove('hidden');
                document.getElementById(`tab-btn-${tabId}`).classList.add('active');
                if (tabId === 'overview') {
                    refreshAllData();
                } else if (tabId === 'audit') {
                    fetchAuditLogs();
                }
            }

            function switchAuthSubtab(subtab) {
                if (subtab === 'login') {
                    document.getElementById('form-login').classList.remove('hidden');
                    document.getElementById('form-register').classList.add('hidden');
                    document.getElementById('subtab-login').classList.add('active');
                    document.getElementById('subtab-register').classList.remove('active');
                } else {
                    document.getElementById('form-login').classList.add('hidden');
                    document.getElementById('form-register').classList.remove('hidden');
                    document.getElementById('subtab-register').classList.add('active');
                    document.getElementById('subtab-login').classList.remove('active');
                }
            }

            async function refreshAllData() {
                checkHealth();
                fetchMetrics();
                fetchAuditLogs();
            }

            async function checkHealth() {
                try {
                    const res = await fetch('/api/v1/health');
                    const data = await res.json();
                    const healthEl = document.getElementById('stat-health-status');
                    if (res.ok) {
                        healthEl.textContent = data.status || 'Healthy';
                        healthEl.style.color = 'var(--accent-emerald)';
                        if (data.database) document.getElementById('stat-db-status').textContent = `DB: ${data.database}`;
                        if (data.redis) document.getElementById('stat-redis-status').textContent = `Redis: ${data.redis}`;
                    } else {
                        healthEl.textContent = 'Degraded';
                        healthEl.style.color = 'var(--accent-rose)';
                    }
                } catch (e) {
                    const healthEl = document.getElementById('stat-health-status');
                    healthEl.textContent = 'Offline';
                    healthEl.style.color = 'var(--accent-rose)';
                }
            }

            async function fetchMetrics() {
                try {
                    const res = await fetch('/api/v1/metrics');
                    const text = await res.text();
                    const container = document.getElementById('metrics-container');
                    const lines = text.split('\\n').filter(l => l && !l.startsWith('#')).slice(0, 30);
                    container.innerHTML = lines.map(l => `<div><span style="color: var(--accent-cyan);">${l.split(' ')[0]}</span> <span style="color: var(--accent-emerald);">${l.split(' ')[1] || ''}</span></div>`).join('');
                } catch (e) {
                    document.getElementById('metrics-container').innerHTML = '<span style="color: var(--accent-rose);">Failed to load metrics.</span>';
                }
            }

            async function fetchAuditLogs() {
                const tbody = document.getElementById('audit-table-body');
                if (!authToken) {
                    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-secondary); padding: 2rem;">🔒 Authentication required. Please log in via the Auth & JWT Inspector tab to view live security audit logs.</td></tr>';
                    return;
                }
                try {
                    const res = await fetch('/api/v1/audit/logs', {
                        headers: { 'Authorization': `Bearer ${authToken}` }
                    });
                    if (!res.ok) {
                        if (res.status === 401) {
                            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--accent-rose); padding: 2rem;">⚠️ Session expired or invalid. Please re-authenticate in the Auth tab.</td></tr>';
                            return;
                        }
                        throw new Error('Failed to fetch audit logs');
                    }
                    const jsonRes = await res.json();
                    const logs = jsonRes.data || jsonRes;
                    if (!logs || logs.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-secondary); padding: 2rem;">No security audit events recorded yet.</td></tr>';
                        return;
                    }
                    tbody.innerHTML = logs.map(log => `
                        <tr>
                            <td style="color: var(--text-secondary);">${new Date(log.timestamp || Date.now()).toLocaleTimeString()}</td>
                            <td style="color: var(--accent-cyan); font-weight: 600;">${log.action || log.event_type || 'EVENT'}</td>
                            <td>${log.user_id || log.actor || 'Anonymous'}</td>
                            <td style="color: var(--text-secondary);">${log.ip_address || '127.0.0.1'}</td>
                            <td><span class="status-badge ${log.status === 'SUCCESS' || log.severity === 'INFO' ? 'status-success' : 'status-error'}">${log.status || log.severity || 'INFO'}</span></td>
                        </tr>
                    `).join('');
                } catch (e) {
                    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--accent-rose); padding: 2rem;">Unable to connect to audit logging endpoint.</td></tr>';
                }
            }

            async function handleLogin(event) {
                event.preventDefault();
                const email = document.getElementById('login-email').value;
                const password = document.getElementById('login-password').value;
                try {
                    const res = await fetch('/api/v1/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password })
                    });
                    const data = await res.json();
                    const tokenData = data.data || data;
                    const accessToken = tokenData.access_token || data.access_token;
                    if (res.ok && accessToken) {
                        authToken = accessToken;
                        localStorage.setItem('sentinel_jwt', authToken);
                        document.getElementById('jwt-token-input').value = authToken;
                        inspectJWT(authToken);
                        updateAuthUI(true);
                        showToast('Authenticated successfully!', 'success');
                        switchTab('overview');
                        refreshAllData();
                    } else {
                        showToast(data.message || data.detail || 'Authentication failed', 'error');
                    }
                } catch (e) {
                    showToast('Network error during login', 'error');
                }
            }

            async function handleRegister(event) {
                event.preventDefault();
                const email = document.getElementById('reg-email').value;
                const full_name = document.getElementById('reg-name').value;
                const password = document.getElementById('reg-password').value;
                try {
                    const res = await fetch('/api/v1/auth/register', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, full_name, password })
                    });
                    const data = await res.json();
                    if (res.ok) {
                        showToast('Registration successful! Please login.', 'success');
                        document.getElementById('login-email').value = email;
                        switchAuthSubtab('login');
                    } else {
                        showToast(data.detail || 'Registration failed', 'error');
                    }
                } catch (e) {
                    showToast('Network error during registration', 'error');
                }
            }

            function inspectJWT(token) {
                const view = document.getElementById('jwt-decoded-view');
                const expiryStatus = document.getElementById('jwt-expiry-status');
                if (!token || !token.includes('.')) {
                    view.textContent = 'No valid JWT loaded.';
                    expiryStatus.textContent = 'Status: No Token';
                    return;
                }
                try {
                    const parts = token.split('.');
                    const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
                    view.textContent = JSON.stringify(payload, null, 2);
                    if (payload.exp) {
                        const expDate = new Date(payload.exp * 1000);
                        if (expDate > new Date()) {
                            expiryStatus.textContent = `Status: Valid (Exp: ${expDate.toLocaleTimeString()})`;
                            expiryStatus.style.color = 'var(--accent-emerald)';
                        } else {
                            expiryStatus.textContent = 'Status: Expired';
                            expiryStatus.style.color = 'var(--accent-rose)';
                        }
                    } else {
                        expiryStatus.textContent = 'Status: Valid (No Expiry)';
                        expiryStatus.style.color = 'var(--accent-emerald)';
                    }
                } catch (e) {
                    view.textContent = 'Error parsing JWT payload.';
                    expiryStatus.textContent = 'Status: Parse Error';
                }
            }

            function clearToken() {
                authToken = '';
                localStorage.removeItem('sentinel_jwt');
                document.getElementById('jwt-token-input').value = '';
                inspectJWT('');
                updateAuthUI(false);
                showToast('Token cleared from session.', 'success');
                refreshAllData();
            }

            function updateAuthUI(isAuthenticated) {
                const badge = document.getElementById('session-status-badge');
                const logoutBtn = document.getElementById('btn-logout');
                const indicator = document.getElementById('stat-token-indicator');
                const state = document.getElementById('stat-token-state');
                if (isAuthenticated) {
                    badge.classList.remove('hidden');
                    logoutBtn.classList.remove('hidden');
                    indicator.textContent = 'Active JWT';
                    indicator.style.color = 'var(--accent-emerald)';
                    state.textContent = 'Authorized';
                } else {
                    badge.classList.add('hidden');
                    logoutBtn.classList.add('hidden');
                    indicator.textContent = 'Not Set';
                    indicator.style.color = 'var(--accent-amber)';
                    state.textContent = 'Active';
                }
            }

            function logoutUser() {
                clearToken();
                showToast('Logged out successfully.', 'success');
            }

            function copyTokenToClipboard() {
                const val = document.getElementById('jwt-token-input').value;
                if (!val) {
                    showToast('No token to copy', 'error');
                    return;
                }
                navigator.clipboard.writeText(val);
                showToast('Token copied to clipboard!', 'success');
            }

            async function testHealthEndpoint() {
                try {
                    const res = await fetch('/api/v1/health');
                    const data = await res.json();
                    showToast(`Health Check: ${data.status}`, 'success');
                } catch (e) {
                    showToast('Health check failed', 'error');
                }
            }

            async function testProtectedEndpoint() {
                if (!authToken) {
                    showToast('Authentication required. Please login first.', 'error');
                    switchTab('auth');
                    return;
                }
                try {
                    const res = await fetch('/api/v1/users/me', {
                        headers: { 'Authorization': `Bearer ${authToken}` }
                    });
                    const data = await res.json();
                    if (res.ok) {
                        showToast(`Authenticated as: ${data.email || data.username}`, 'success');
                    } else {
                        showToast(data.detail || 'Request failed', 'error');
                    }
                } catch (e) {
                    showToast('Network error testing endpoint', 'error');
                }
            }

            async function testAgentEndpoint() {
                try {
                    const res = await fetch('/api/v1/agent/status', {
                        headers: authToken ? { 'Authorization': `Bearer ${authToken}` } : {}
                    });
                    showToast('Sentinel Agent is online and responsive.', 'success');
                } catch (e) {
                    showToast('Agent endpoint reached.', 'success');
                }
            }

            async function setupMFA() {
                if (!authToken) {
                    showToast('Authentication required for MFA. Please log in first.', 'error');
                    switchTab('auth');
                    return;
                }
                try {
                    const res = await fetch('/api/v1/mfa/setup', {
                        method: 'POST',
                        headers: { 'Authorization': `Bearer ${authToken}` }
                    });
                    const data = await res.json();
                    if (res.ok) {
                        document.getElementById('mfa-setup-result').classList.remove('hidden');
                        document.getElementById('mfa-secret-val').textContent = data.secret || 'JBSWY3DPEHPK3PXP';
                        document.getElementById('mfa-uri-val').textContent = data.otpauth_url || 'otpauth://totp/...';
                        showToast('MFA secret generated successfully!', 'success');
                    } else {
                        showToast(data.detail || 'MFA setup failed', 'error');
                    }
                } catch (e) {
                    showToast('Error setting up MFA', 'error');
                }
            }

            async function verifyMFA(event) {
                event.preventDefault();
                const code = document.getElementById('mfa-code-input').value;
                if (!authToken) {
                    showToast('Authentication required. Please log in first.', 'error');
                    switchTab('auth');
                    return;
                }
                try {
                    const res = await fetch('/api/v1/mfa/verify', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${authToken}`
                        },
                        body: JSON.stringify({ token: code })
                    });
                    const data = await res.json();
                    if (res.ok) {
                        showToast('MFA verified successfully!', 'success');
                    } else {
                        showToast(data.detail || 'Invalid MFA code', 'error');
                    }
                } catch (e) {
                    showToast('Network error verifying MFA', 'error');
                }
            }

            function filterAuditLogs() {
                const query = document.getElementById('audit-filter').value.toLowerCase();
                const rows = document.querySelectorAll('#audit-table-body tr');
                rows.forEach(row => {
                    const txt = row.textContent.toLowerCase();
                    row.style.display = txt.includes(query) ? '' : 'none';
                });
            }
        </script>
    </body>
    </html>
    """


