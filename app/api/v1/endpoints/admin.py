from fastapi import APIRouter, Depends
from app.api.deps import RoleChecker
from app.core.responses import api_response

router = APIRouter()

@router.post("/admin-only")
async def admin_action(current_user=Depends(RoleChecker(["admin"]))):
    return api_response(status="success", message="Admin action performed")
