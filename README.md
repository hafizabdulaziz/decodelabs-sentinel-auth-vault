# Sentinel Auth Vault

Enterprise-Grade Zero Trust Authentication & Autonomous Security Engine.

## Overview
Sentinel Auth Vault provides a secure, scalable, and autonomous authentication framework designed for modern enterprise architectures. It integrates advanced security primitives including Multi-Factor Authentication (TOTP), Role-Based Access Control (RBAC), distributed session revocation (Redis), and an autonomous AI security agent.

## Core Features
- **Security:** Argon2id password hashing, JWT stateless authentication, Security Headers.
- **MFA:** TOTP support with QR code setup and verification.
- **RBAC:** Fine-grained role and permission management.
- **Autonomous IDS:** AI-powered security agent for anomaly detection and audit logging.
- **Performance:** Asynchronous persistence (SQLAlchemy 2.0 + AsyncPG) and sliding-window rate limiting.
- **Observability:** Prometheus metrics, Structlog JSON logging, and Health Diagnostics.
- **CI/CD:** Automated testing, linting (Ruff), and Docker build verification.

## Architecture
- **API:** FastAPI
- **Database:** PostgreSQL (Async)
- **Cache:** Redis
- **Documentation:** Scalar (Interactive OpenAPI)

## Installation & Setup
### Prerequisites
- Docker & Docker Compose
- Python 3.13+

### Quick Start
1. Clone the repository.
2. Configure `.env` file based on `.env.example`.
3. Run `docker-compose up -d`.
4. Access API Docs/UI at `http://localhost:8000/scalar`.

## Documentation
- **Interactive UI:** [http://localhost:8000/scalar](http://localhost:8000/scalar)
- **Metrics:** `GET /api/v1/metrics`
- **Health:** `GET /api/v1/health`

## Development
- **Tests:** `pytest`
- **Linting:** `ruff check .`
