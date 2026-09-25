from fastapi import HTTPException, Request, status

from app.db.session import async_session
from app.services.audit_logger import log_event


async def detect_anomalies(request: Request, payload: dict):
    # Basic IDS: Detect suspicious login patterns
    if "password" in payload and payload.get("password") == "admin123":
        async with async_session() as db:
            await log_event(db, request, "SUSPICIOUS_LOGIN", "auth", {"email": payload.get("email")}, severity="CRITICAL")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Suspicious activity detected")
