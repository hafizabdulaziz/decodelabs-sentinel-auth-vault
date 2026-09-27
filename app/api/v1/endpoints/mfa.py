import logging

import pyotp
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.responses import api_response
from app.models.mfa import MFAModel
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/setup")
async def setup_mfa(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MFAModel).where(MFAModel.user_id == current_user.id))
    mfa = result.scalars().first()
    
    if not mfa:
        secret = pyotp.random_base32()
        mfa = MFAModel(user_id=current_user.id, secret=secret, is_enabled=False)
        db.add(mfa)
        await db.commit()
        await db.refresh(mfa)
    else:
        secret = mfa.secret

    totp = pyotp.TOTP(secret)
    otpauth_url = totp.provisioning_uri(name=current_user.email, issuer_name="Sentinel Auth Vault")
    
    return api_response(
        status="success",
        data={
            "secret": secret,
            "otpauth_url": otpauth_url
        },
        message="MFA setup generated"
    )

@router.post("/verify")
async def verify_mfa(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    token = None
    try:
        body = await request.json()
        token = body.get("token") or body.get("code")
    except (ValueError, TypeError):
        try:
            form = await request.form()
            token = form.get("token") or form.get("code")
        except (ValueError, TypeError) as exc:
            logger.warning("Failed to parse request body or form: %s", exc)
            token = None

    if not token:
        token = request.query_params.get("token") or request.query_params.get("code")

    result = await db.execute(select(MFAModel).where(MFAModel.user_id == current_user.id))
    mfa = result.scalars().first()
    
    if not mfa or not pyotp.TOTP(mfa.secret).verify(token):
        raise HTTPException(status_code=400, detail="Invalid token")
        
    mfa.is_enabled = True
    await db.commit()
    return api_response(status="success", message="MFA verified and enabled")
