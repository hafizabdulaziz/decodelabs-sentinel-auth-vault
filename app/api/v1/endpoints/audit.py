from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import RoleChecker
from app.core.responses import api_response
from app.db.session import get_db
from app.models.audit import AuditLog

router = APIRouter()

@router.get("/logs")
async def get_audit_logs(
    db: AsyncSession = Depends(get_db), 
    current_user=Depends(RoleChecker(["admin"]))
):
    result = await db.execute(select(AuditLog).order_by(AuditLog.created_at.desc()))
    logs = result.scalars().all()
    return api_response(status="success", data=logs)
