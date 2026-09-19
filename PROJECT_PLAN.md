# Project Plan - Sentinel Auth Vault

## Master Blueprint

### PART 1: CORE REQUIREMENTS (PHASES 1 TO 10)
- **Phase 1: Repository Architecture & Enterprise Infrastructure**
  - [x] Step 1.1: Local workspace initialization. Setup pyproject.toml (Poetry/UV), .gitignore (shielding .env, __pycache__, .venv, .pytest_cache), and link remote origin.
  - [ ] Step 1.2: Directory scaffold generation: app/api/v1/endpoints/, app/core/, app/db/, app/models/, app/schemas/, app/services/, migrations/, tests/, scripts/.
  - [ ] Step 1.3: Production Dockerfile (multi-stage build) aur docker-compose.yml (PostgreSQL + Redis + App container setup) configure karna.
  - [ ] Step 1.4: Enterprise environment manager app/core/config.py using pydantic-settings. .env.example file sync karna.

- **Phase 2: Async Relational Persistence Engine**
  - [ ] Step 2.1: Async SQLAlchemy 2.0 engine aur session factory (app/db/session.py) construct karna.
  - [ ] Step 2.2: Async Alembic migrations setup (migrations/env.py) with dynamic connection handling.
  - [ ] Step 2.3: Base declarative ORM model (app/db/base.py) with dynamic created_at aur updated_at UTC mixins.
  - [ ] Step 2.4: Initial migration run karke database connection verify karna.

- **Phase 3: Cryptographic Password Storage (OWASP Argon2id Enforcement)**
  - [ ] Step 3.1: app/core/security.py me passlib with Argon2id configuration initialize karna.
  - [ ] Step 3.2: OWASP parameters set karna: Memory cost 64MB (m=65536), Time cost 3 iterations (t=3), Parallelism 1 thread (p=1).
  - [ ] Step 3.3: Password hashing aur 128-bit random salt verification logic implement karna.
  - [ ] Step 3.4: Strict password complexity validator create karna (min 8 chars, 1 uppercase, 1 special char, 1 number).

- **Phase 4: User Data Domain & Pydantic Contracts**
  - [ ] Step 4.1: User ORM Model design (id, uuid, email, hashed_password, is_active, is_superuser, created_at).
  - [ ] Step 4.2: Pydantic v2 schemas create karna (UserCreate, UserRead, UserUpdate, PasswordChange).
  - [ ] Step 4.3: Email normalization aur sanitization utility add karna.
  - [ ] Step 4.4: Alembic migration generate karke user table execute karna.

- **Phase 5: Stateless JWT Lifecycle Architecture**
  - [ ] Step 5.1: Cryptographic JWT token engine (app/core/security.py) using python-jose / PyJWT.
  - [ ] Step 5.2: Access Token (15 mins exp) & Refresh Token (7 days exp) payload structures define karna.
  - [ ] Step 5.3: Token signing with HMAC-SHA256 (HS256) and dynamic expiration verification logic.
  - [ ] Step 5.4: Unit tests write karna for token creation, decoding, and signature tampering detection.

- **Phase 6: Core Authentication API Layer**
  - [ ] Step 6.1: POST /api/v1/auth/register endpoint build karna with Argon2id pre-save hashing.
  - [ ] Step 6.2: POST /api/v1/auth/login endpoint build karna with credential verification and JWT generation.
  - [ ] Step 6.3: Standardized JSON API Response Wrapper (status, data, message, timestamp) design karna.
  - [ ] Step 6.4: HTTP 401 (Unauthorized) & HTTP 422 (Unprocessable Entity) exception handlers build karna.

- **Phase 7: Middleware Gatekeeper & Protected API Perimeter**
  - [ ] Step 7.1: OAuth2 Bearer scheme extractor dependency (app/api/deps.py) implement karna.
  - [ ] Step 7.2: Custom Auth Middleware create karna jo HTTP Authorization: Bearer <token> inspect kare.
  - [ ] Step 7.3: Protected Endpoint GET /api/v1/users/me create karna jo user identity return kare.
  - [ ] Step 7.4: Tests write karna: Unauthenticated requests instantly 401 Unauthorized return karein.

- **Phase 8: Database-Driven Refresh Token Rotation**
  - [ ] Step 8.1: RefreshToken database model design (id, user_id, token_hash, expires_at, is_revoked).
  - [ ] Step 8.2: Endpoint POST /api/v1/auth/refresh implement karna for seamless token renewal.
  - [ ] Step 8.3: Automatic old refresh token revocation logic write karna.
  - [ ] Step 8.4: Database migration and token rotation test cases execute karna.

- **Phase 9: Automated Test Suite Harness**
  - [ ] Step 9.1: pytest-asyncio testing harness configure karna with PostgreSQL test container.
  - [ ] Step 9.2: Unit tests write karna for Argon2id hashing, JWT signing, and Pydantic validation.
  - [ ] Step 9.3: End-to-end integration tests for Registration -> Login -> Access Protected Route flow.
  - [ ] Step 9.4: Coverage report run karke 100% pass status verify karna.

- **Phase 10: Interactive OpenAPI Engine (Scalar UI)**
  - [ ] Step 10.1: Scalar UI integration in FastAPI (app/main.py) with custom dark enterprise theme.
  - [ ] Step 10.2: OpenAPI metadata tags, Bearer Security Scheme, and response schemas configure karna.
  - [ ] Step 10.3: Scalar UI interface test run karna (endpoints execution and payload checks).
  - [ ] Step 10.4: Milestone 1 PDF Compliance Audit Complete.

### PART 2: ADVANCED ENTERPRISE & AUTONOMOUS ENGINE (PHASES 11 TO 20)
- **Phase 11: Multi-Factor Authentication Engine (TOTP)**
- **Phase 12: Role-Based Access Control (RBAC) & Fine-Grained Permissions**
- **Phase 13: Distributed Session Revocation Engine (Redis)**
- **Phase 14: Sliding-Window Rate Limiting & Account Protection**
- **Phase 15: Cryptographic Audit Logging & Intrusion Detection (IDS)**
- **Phase 16: Autonomous Sentinel AI Security Agent**
- **Phase 17: Observability, Structured Logging & Health Diagnostics**
- **Phase 18: Security Perimeter Hardening & Headers**
- **Phase 19: CI/CD Pipeline & Automated Quality Assurance**
- **Phase 20: Production Showcase & Master Documentation**
