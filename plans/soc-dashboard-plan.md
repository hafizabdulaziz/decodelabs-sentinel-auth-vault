# Plan: Enterprise Security Operations Center (SOC) Dashboard

## Objective
Sentinel Auth Vault ke liye ek high-impact, professional Enterprise Security Operations Center (SOC) HTML/JS Dashboard banana jo root route (`/`) par serve ho. Yeh dashboard dark glassmorphism theme, real-time metrics, interactive auth & MFA testing forms, JWT token viewer, aur live security audit logs display karega.

---

## Key Features & UI Components

1. **Design System & Theme (Dark Glassmorphism)**
   - Background: Deep slate/dark navy gradient (`#0b0f19` to `#1e1b4b`).
   - Glassmorphism cards: `backdrop-filter: blur(16px)`, translucent background (`rgba(15, 23, 42, 0.7)`), subtle glowing borders (`border border-slate-700/50`).
   - Styling & Icons: Tailwind CSS v3 (via CDN), Google Fonts (Inter / JetBrains Mono), and Lucide / FontAwesome icons.

2. **Top Navigation Bar**
   - Brand Logo & Sentinel Status Badge (Live pulsing green "SECURE" indicator).
   - Quick Links: API Docs (`/docs`), Scalar API Reference (`/scalar`), GitHub Repo.
   - Active user session indicator & Logout / Token clear button.

3. **Dashboard Modules / Tabs**
   - **Overview / Metrics Tab**:
     - Stat Cards: API Health Status, Active Sessions, Blocked Rate-Limit IPs, Sentinel Agent Status.
     - Live System Telemetry graphs/cards (CPU, Memory, Request Latency simulated or fetched from `/api/v1/metrics`).
   - **Authentication & Testing Tab**:
     - Interactive Registration & Login forms with real-time API feedback.
     - JWT Token Viewer: Automatically captures access token, decodes JWT payload (Header, Payload, Expiry) in real-time, and allows copying or testing.
   - **MFA Verification Tab**:
     - Interactive MFA setup (TOTP QR code simulation/secret key) & Verification code entry form.
   - **Security Audit Logs Tab**:
     - Real-time table showing security audit events (user logins, failed attempts, admin actions, IP tracking) fetched from `/api/v1/audit`.
     - Severity badges (INFO, WARNING, CRITICAL).

---

## Implementation Steps

1. **Update `app/main.py` Root Endpoint (`/`)**:
   - Replace the simple placeholder HTML with a fully self-contained, robust HTML/JS Single Page Application (SPA) dashboard that communicates with `/api/v1/...` endpoints.
   
2. **Dashboard JavaScript Logic**:
   - `fetch` API wrappers for Auth (`/api/v1/auth/login`, `/api/v1/auth/register`), Health (`/api/v1/health`), Metrics (`/api/v1/metrics`), Audit Logs (`/api/v1/audit`), and MFA (`/api/v1/mfa/...`).
   - LocalStorage management for JWT bearer tokens so users can test authenticated endpoints seamlessly.
   - JWT Decoder utility (Base64 decoding of payload JSON) running entirely client-side.
   - Auto-refresh mechanism for health status and audit logs every 10 seconds.

3. **Verification**:
   - Run pytest and ensure existing backend tests pass.
   - Test the root endpoint `/` via browser or curl to verify HTML rendering and API integration.
