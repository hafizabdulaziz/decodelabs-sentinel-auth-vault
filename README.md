# Sentinel Auth Vault

Production-ready, zero-trust authentication engine and security management platform built with Python 3.13 and FastAPI. The service provides enterprise-grade identity lifecycle management, token rotation, multi-factor authentication (TOTP), security audit logging, sliding-window rate limiting, and an integrated SOC dashboard.

Designed using asynchronous I/O and non-blocking database access, this architecture handles active session revocation, agent status telemetry, and centralized security monitoring for high-assurance microservices.

---

## Technical Stack & Architecture

- **Framework**: FastAPI (Python 3.13, Async I/O)
- **Database & ORM**: PostgreSQL / Neon Serverless via SQLAlchemy 2.0 (AsyncSession)
- **Database Migrations**: Alembic (Asynchronous migration pipeline)
- **Caching & Revocation**: Redis (Sliding-window rate limiting & JWT revocation blacklist)
- **Security & Cryptography**: Password hashing via Argon2id, JWT auth (Access/Refresh token rotation), PyOTP (TOTP 2FA)
- **Observability**: Prometheus metrics, structured JSON logging, and system health diagnostics
- **User Interface**: Integrated SOC Dashboard and Dark-Mode OpenAPI/Swagger docs

---

## Core Features & System Capabilities

1. **Authentication & Session Lifecycle**:
   - Operator registration, authentication, and JWT pair issuance (Access/Refresh tokens).
   - Refresh token rotation with database persistence and real-time verification.
   - Active session logout with instant Redis token blacklisting.

2. **Multi-Factor Authentication (MFA/TOTP)**:
   - Secret key generation, QR code provisioning, and time-based OTP validation.
   - Enforced step-up authentication for elevated administrative actions.

3. **Audit Logging & Security Operations**:
   - Immutable security audit event trail recording privileged actions and auth states.
   - Autonomous security agent health monitoring and query status endpoints.
   - Centralized SOC Dashboard interface (`/`) for real-time overview.

4. **Rate Limiting & Defense Mechanisms**:
   - Redis-backed sliding-window rate limiting interceptor.
   - Hardened HTTP headers middleware (CORS, CSP, XSS-Protection, HSTS).
   - Input sanitization and payload schema validation via Pydantic v2.

5. **Telemetry & System Health**:
   - Dedicated health check (`/api/v1/health`) and Prometheus operational metrics (`/api/v1/metrics`).

---

## API Endpoints Reference

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register a new operator account | No |
| `POST` | `/api/v1/auth/login` | Authenticate and obtain JWT access & refresh tokens | No |
| `POST` | `/api/v1/auth/refresh` | Refresh expired access tokens using rotation | No |
| `POST` | `/api/v1/auth/logout` | Revoke active session and blacklist JWT | Yes (Bearer) |
| `GET` | `/api/v1/users/me` | Retrieve authenticated operator profile | Yes (Bearer) |
| `POST` | `/api/v1/mfa/setup` | Generate TOTP secret & QR configuration | Yes (Bearer) |
| `POST` | `/api/v1/mfa/verify` | Verify TOTP verification code | Yes (Bearer) |
| `GET` | `/api/v1/audit/logs` | Retrieve immutable security audit event trail | Yes (Admin Role) |
| `POST` | `/api/v1/admin/actions` | Execute privileged administrative operations | Yes (Admin Role) |
| `GET` | `/api/v1/agent/status` | Query autonomous security agent health & status | Yes / Optional |
| `GET` | `/api/v1/health` | System health check (DB, Redis, Core) | No |
| `GET` | `/api/v1/metrics` | Prometheus operational telemetry metrics | No |

---

## Local Development & Setup

### Prerequisites
- Python 3.13+
- Redis Server
- PostgreSQL / Neon Postgres DB URL

### Installation Steps

1. **Clone Repository & Setup Environment**:
   ```bash
   git clone [https://github.com/hafizabdulaziz/decodelabs-sentinel-auth-vault.git](https://github.com/hafizabdulaziz/decodelabs-sentinel-auth-vault.git)
   cd decodelabs-sentinel-auth-vault
   python -m venv .venv
   
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
Install Dependencies:

Bash
pip install poetry
poetry install
Environment Configuration:
Create a .env file in the root directory following .env.example:

Code snippet
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/sentinel_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secret-jwt-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
Run Migrations & Launch Application:

Bash
# Run database migrations
alembic upgrade head

# Quick start script (Windows)
run.bat

# Or launch directly via uvicorn
uvicorn app.main:app --reload
Interface Access:

SOC Dashboard: http://localhost:8000/

Interactive API Docs (Swagger UI): http://localhost:8000/docs

Prometheus Metrics: http://localhost:8000/api/v1/metrics

Development & Testing
Automated testing and linting instructions:

Bash
# Run test suite
.venv\Scripts\python -m pytest

# Run code linter
ruff check .
