from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.user import User
from app.models.token import RefreshToken
from app.schemas.user import UserCreate, UserRead
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.core.responses import api_response
from app.core.validators import verify_password_strength
from app.core.utils import normalize_email
from datetime import datetime, timedelta, timezone
from app.core.config import settings

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
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

@router.post("/login")
async def login(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    email = normalize_email(user_in.email)
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
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
