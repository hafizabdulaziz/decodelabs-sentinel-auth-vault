
import pyotp
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.responses import api_response
from app.models.mfa import MFAModel
from app.models.user import User

router = APIRouter()

@router.post("/verify")
async def verify_mfa(token: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MFAModel).where(MFAModel.user_id == current_user.id))
    mfa = result.scalars().first()
    
    if not mfa or not pyotp.TOTP(mfa.secret).verify(token):
        raise HTTPException(status_code=400, detail="Invalid token")
        
    mfa.is_enabled = True
    await db.commit()
    return api_response(status="success", message="MFA verified and enabled")
