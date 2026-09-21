from fastapi import APIRouter, Depends, Header
from app.api.deps import get_current_user
from app.services.token_blacklist import blacklist_token
from app.core.responses import api_response

router = APIRouter()

@router.post("/logout")
async def logout(authorization: str = Header(...), current_user=Depends(get_current_user)):
    token = authorization.replace("Bearer ", "")
    await blacklist_token(token)
    return api_response(status="success", message="Logged out successfully")
