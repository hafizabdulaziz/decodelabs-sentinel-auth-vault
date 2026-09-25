from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.responses import api_response
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.db.session import get_db
from app.models.token import RefreshToken

router = APIRouter()

@router.post("/refresh")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # Check if token is revoked in DB
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == refresh_token))
    token_db = result.scalars().first()
    if not token_db or token_db.is_revoked or token_db.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired or revoked",
        )
    
    # Revoke old token and generate new pair
    token_db.is_revoked = True
    await db.commit()
    
    new_access = create_access_token(payload.get("sub"))
    new_refresh = create_refresh_token(payload.get("sub"))
    
    return api_response(
        status="success",
        data={"access_token": new_access, "refresh_token": new_refresh}
    )
