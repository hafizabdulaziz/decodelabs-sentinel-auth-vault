from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import RateLimitChecker
from app.core.config import settings
from app.core.responses import api_response
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.core.utils import normalize_email
from app.core.validators import verify_password_strength
from app.db.session import get_db
from app.models.mfa import MFAModel
from app.models.token import RefreshToken
from app.models.user import User
from app.schemas.user import LoginRequest, UserCreate

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimitChecker(limit=5, window=60))])
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        verify_password_strength(user_in.password)
        email = normalize_email(user_in.email)
        
        result = await db.execute(select(User).where(User.email == email))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="User already exists")
        
        user = User(
            email=email,
            hashed_password=get_password_hash(user_in.password)
        )
        db.add(user)
        await db.commit()
        return api_response(status="success", message="User registered successfully")
    except HTTPException:
        raise
    except (SQLAlchemyError, ValueError, TypeError) as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error during registration: {e!s}")

@router.post("/login", dependencies=[Depends(RateLimitChecker(limit=5, window=60))])
async def login(login_in: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        email = normalize_email(login_in.email)
        password = login_in.password
            
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Check MFA
        mfa_result = await db.execute(select(MFAModel).where(MFAModel.user_id == user.id))
        mfa = mfa_result.scalars().first()
        if mfa and mfa.is_enabled:
            return api_response(status="mfa_required", message="MFA verification required")
        
        access_token = create_access_token(user.email)
        refresh_token = create_refresh_token(user.email)
        
        # Store refresh token
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        new_token = RefreshToken(
            user_id=user.id,
            token_hash=refresh_token,
            expires_at=expires_at
        )
        db.add(new_token)
        await db.commit()
        
        return api_response(
            status="success", 
            data={"access_token": access_token, "refresh_token": refresh_token}
        )
    except HTTPException:
        raise
    except (SQLAlchemyError, ValueError, TypeError) as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error during login: {e!s}")
