from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.token import RefreshToken
from app.models.user import User
from app.core.security import verify_token, create_access_token, create_refresh_token, get_password_hash
from app.core.responses import api_response
from datetime import datetime, timezone

router = APIRouter()

@router.post("/refresh")
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    email = payload.get("sub")
    # Check if token exists and is not revoked in DB
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == refresh_token))
    token_db = result.scalars().first()
    
    if not token_db or token_db.is_revoked or token_db.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired or revoked")
        
    # Revoke old token
    token_db.is_revoked = True
    
    # Generate new tokens
    new_access_token = create_access_token(email)
    new_refresh_token = create_refresh_token(email)
    
    # Store new refresh token
    new_token_db = RefreshToken(
        user_id=token_db.user_id,
        token_hash=new_refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7) # simplified
    )
    db.add(new_token_db)
    await db.commit()
    
    return api_response(
        status="success",
        data={"access_token": new_access_token, "refresh_token": new_refresh_token}
    )
