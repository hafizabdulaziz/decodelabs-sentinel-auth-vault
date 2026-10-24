# Sentinel Auth Vault

An asynchronous authentication and access control backend service built with FastAPI and SQLAlchemy (Async).

## Overview

Sentinel Auth Vault provides identity management, access control, and defense-in-depth security mechanisms for API architectures. The service implements JWT authentication lifecycle management, Multi-Factor Authentication (MFA with TOTP), Role-Based Access Control (RBAC), Redis-backed sliding-window rate limiting, account lockout policies, custom security headers, and Prometheus telemetry metrics.

## Key Features

- **Authentication & Token Lifecycle**: User registration, login verification, token rotation, and explicit logout with token blacklisting.
- **Multi-Factor Authentication (MFA)**: TOTP secret provisioning, QR code generation via `pyotp`, and second-factor verification workflows.
- **Role-Based Access Control (RBAC)**: Fine-grained permission verification isolating standard user privileges from administrative routes.
- **Defensive Security Controls**: Sliding-window rate limiting against brute-force attacks, automated account lockout on consecutive failed login attempts, input sanitization via `bleach`, and security headers middleware.
- **Observability & Diagnostics**: Health check endpoint (`/health`), Prometheus metrics export (`/metrics`), SOC dashboard interface, and structured logging via `structlog`.

## Technology Stack

- **Framework**: FastAPI (0.115+) running on the Uvicorn ASGI server
- **Database & ORM**: SQLAlchemy 2.0+ (AsyncEngine) with Alembic schema migrations (`aiosqlite` for local development, `asyncpg` for PostgreSQL)
- **Caching & State Storage**: Redis (used for sliding-window rate limiting, session tracking, and token blacklisting)
- **Security & Cryptography**:
  - Password Hashing: Argon2id (`passlib`)
  - Token Management: JWT (`python-jose`) with refresh token rotation
  - Multi-Factor Authentication: Time-based One-Time Passwords (`pyotp`)
  - Input Sanitization: `bleach`
- **Telemetry & Logging**: Prometheus (`prometheus-fastapi-instrumentator`) and structured logging with `structlog`
- **Dependency Management**: Poetry
- **Testing & Static Analysis**: Pytest, `pytest-asyncio`, HTTPX, and Ruff

## API Reference

| Endpoint | Method | Description | Authentication |
| :--- | :---: | :--- | :--- |
| `/api/v1/auth/register` | `POST` | Register a new user account (rate limited) | None |
| `/api/v1/auth/login` | `POST` | Authenticate credentials and issue JWT tokens (rate limited) | None |
| `/api/v1/auth/refresh` | `POST` | Rotate access token using a valid refresh token | Refresh Token |
| `/api/v1/auth/logout` | `POST` | Revoke and blacklist current session tokens | Bearer Token |
| `/api/v1/users/me` | `GET` | Retrieve the authenticated user's profile | Bearer Token |
| `/api/v1/mfa/setup` | `POST` | Generate TOTP secret and QR code for MFA setup | Bearer Token |
| `/api/v1/mfa/verify` | `POST` | Verify and activate TOTP multi-factor authentication | Bearer Token |
| `/api/v1/admin/admin-only` | `POST` | Execute administrative operation | Admin RBAC |
| `/api/v1/agent/execute` | `POST` | Execute security agent operations | Bearer Token |
| `/api/v1/audit/logs` | `GET` | Query security audit log records | Bearer Token |
| `/api/v1/health` | `GET` | Retrieve system operational health status | None |
| `/api/v1/metrics` | `GET` | Export Prometheus telemetry and performance metrics | None |

## Environment Setup & Configuration

### Prerequisites
- Python 3.13+
- Poetry
- Redis server (optional fallback available for local development/testing)

### Environment Configuration

Copy `.env.example` to `.env` and set the required variables:

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

3. Start the application server (or run `run.bat` on Windows):
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## Testing & Quality Assurance

### Run Automated Tests
Execute the asynchronous test suite using pytest:
```bash
poetry run pytest
```
*On Windows, you can alternatively run `test.bat`.*

### Code Quality & Linting
Run static analysis and linting via Ruff:
```bash
poetry run ruff check .
```
*On Windows, you can alternatively run `lint.bat`.*
