# Sentinel Auth Vault

Sentinel Auth Vault is a production-ready, asynchronous Python backend service built with FastAPI and SQLAlchemy async. It solves enterprise authentication and access control challenges by providing robust JWT-based authentication, multi-factor authentication (MFA with TOTP), role-based access control (RBAC), Redis-backed sliding-window rate limiting, account lockout mechanisms, security headers middleware, and built-in health/metrics instrumentation.

---

## Key Architecture & Technical Stack

- **Framework:** FastAPI 0.115+ running on Uvicorn async ASGI server.
- **Database & ORM:** SQLAlchemy 2.0+ async engine with Alembic migrations (`aiosqlite` for local/testing, PostgreSQL supported via `asyncpg`).
- **Caching & State:** Redis backend for rate limiting, session management, and token blacklisting.
- **Security & Cryptography:** 
  - Password Hashing: Argon2id (`passlib`)
  - Token Management: JWT (`python-jose`) with rotation and revocation.
  - Multi-Factor Authentication: Time-based One-Time Passwords (`pyotp`) with QR code generation.
  - Defensive Controls: Custom security headers middleware, sliding-window rate limiters, account lockout protection, and input sanitization (`bleach`).
- **Observability & Testing:** Prometheus metrics instrumentation (`prometheus-fastapi-instrumentator`), structured logging (`structlog`), Pytest, pytest-asyncio, and HTTPX.

---

## Core Features & Security Implementations

1. **Authentication & Token Lifecycle:** Secure registration, login, token refresh rotation, and explicit logout with token blacklisting.
2. **Multi-Factor Authentication (MFA):** TOTP secret generation, QR code provisioning, and second-factor verification during authentication workflows.
3. **Role-Based Access Control (RBAC):** Granular permission checks separating regular users from administrative principals.
4. **Resilience & Protection:** Sliding-window rate limiting to mitigate brute-force and DoS attacks, alongside automated account lockout policies after repeated failed attempts.
5. **Production Readiness:** Comprehensive health checks (`/health`), Prometheus metrics (`/metrics`), SOC dashboard interface, and strict security response headers.

---

## API Reference / Route Summary

| Endpoint | Method | Description | Auth Requirement |
| :--- | :---: | :--- | :--- |
| `/api/v1/auth/register` | `POST` | Register a new user account (Rate limited) | None |
| `/api/v1/auth/login` | `POST` | Authenticate user & issue JWT tokens (Rate limited) | None |
| `/api/v1/auth/refresh` | `POST` | Rotate access token using a valid refresh token | Refresh Token |
| `/api/v1/auth/logout` | `POST` | Revoke/blacklist current session tokens | Bearer Token |
| `/api/v1/users/me` | `GET` | Retrieve authenticated user profile | Bearer Token |
| `/api/v1/mfa/setup` | `POST` | Initialize TOTP secret & QR code for MFA | Bearer Token |
| `/api/v1/mfa/verify` | `POST` | Verify and activate TOTP MFA | Bearer Token |
| `/api/v1/admin/admin-only` | `POST` | Execute administrative operation | Admin RBAC |
| `/api/v1/agent/execute` | `POST` | Execute security agent operations | Bearer Token |
| `/api/v1/audit/logs` | `GET` | Query security audit logs | Bearer Token |
| `/api/v1/health` | `GET` | System health status check | None |
| `/api/v1/metrics` | `GET` | Prometheus performance metrics export | None |

---

## Local Setup & Environment Configuration

### Prerequisites
- Python 3.13+
- Poetry (Dependency Management)
- Redis server (optional for local development/testing fallback)

### Configuration
Copy `.env.example` to `.env` and configure the required environment variables:

```env
DATABASE_URL=sqlite+aiosqlite:///./sentinel.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=supersecretkeythatshouldberotated
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Installation & Execution

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Run database migrations:
   ```bash
   poetry run alembic upgrade head
   ```

3. Start the development server (or use `run.bat` on Windows):
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

---

## Automated Testing & Linting Instructions

### Running Tests
Execute the test suite using pytest with asynchronous support:
```bash
poetry run pytest
```
Or use the provided batch script:
```cmd
test.bat
```

### Code Quality & Linting
Run static analysis and lint checks using Ruff:
```bash
poetry run ruff check .
```
Or use the lint script:
```cmd
lint.bat
```
