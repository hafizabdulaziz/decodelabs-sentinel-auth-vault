from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog


async def log_event(
    db: AsyncSession,
    request: Request,
    action: str,
    resource: str,
    payload: dict,
    user_id: str = None,
    severity: str = "INFO"
):
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        payload=payload,
        ip_address=request.client.host,
        severity=severity
    )
    db.add(log)
    await db.commit()
