# Sentinel Auth Vault

Enterprise-Grade Zero Trust Authentication & Autonomous Security Engine.

## Overview
Sentinel Auth Vault is an enterprise-grade, zero-trust authentication and autonomous security platform designed for high-assurance microservices and distributed systems. It features advanced cryptographic password hashing (Argon2id), stateless JWT validation, multi-factor authentication (TOTP), sliding-window rate limiting, Redis-backed token revocation, and an autonomous AI security agent.

---

## Architecture & Tech Stack
- **Framework:** FastAPI (High-performance async Python)
- **Database ORM:** SQLAlchemy 2.0 (AsyncSession) with Alembic migrations
- **Caching & Revocation:** Redis
- **Security Primitives:** Argon2id, JWT, TOTP (PyOTP), HTTPBearer
- **Observability:** Prometheus metrics (`/api/v1/metrics`), Structured JSON logging, Health checks (`/api/v1/health`)
- **Documentation:** Custom Dark-Mode Enterprise Swagger UI (`/docs`)

---

## API Endpoints Reference

| Endpoint | Method | Description | Auth Required |
| :--- | :---: | :--- | :---: |
| `/api/v1/auth/register` | `POST` | Register a new operator account | No |
| `/api/v1/auth/login` | `POST` | Authenticate and obtain JWT access & refresh tokens | No |
| `/api/v1/auth/refresh` | `POST` | Refresh expired access tokens | No |
| `/api/v1/auth/logout` | `POST` | Revoke active session / JWT | Yes (Bearer) |
| `/api/v1/users/me` | `GET` | Retrieve authenticated operator profile | Yes (Bearer) |
| `/api/v1/mfa/setup` | `POST` | Generate TOTP secret & QR configuration | Yes (Bearer) |
| `/api/v1/mfa/verify` | `POST` | Verify TOTP verification code | Yes (Bearer) |
| `/api/v1/audit/logs` | `GET` | Retrieve immutable security audit event trail | Yes (Admin Role) |
| `/api/v1/admin/actions` | `POST` | Execute privileged administrative operations | Yes (Admin Role) |
| `/api/v1/agent/status` | `GET` | Query autonomous security agent health & status | Yes / Optional |
| `/api/v1/health` | `GET` | System health check (DB, Redis, Core) | No |
| `/api/v1/metrics` | `GET` | Prometheus operational telemetry metrics | No |

---

## Installation & Setup

### Prerequisites
- Python 3.13+
- Docker & Docker Compose (optional for containerized deployment)

### Local Quick Start (`run.bat`)
1. Clone the repository and navigate to the project directory.
2. Set up virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install poetry
   poetry install
   ```
3. Run the application using `run.bat` or directly via uvicorn:
   ```bash
   run.bat
   ```
4. Open the Enterprise SOC Dashboard and Interactive API Docs at:
   - **SOC Dashboard & Interface:** [http://localhost:8000/](http://localhost:8000/)
   - **Swagger UI (Interactive Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Metrics Telemetry:** [http://localhost:8000/api/v1/metrics](http://localhost:8000/api/v1/metrics)

---

## Development & Testing
- **Run Test Suite:**
  ```bash
  .venv\Scripts\python -m pytest
  ```
- **Run Linter:**
  ```bash
  ruff check .
  ```
