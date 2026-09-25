from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.user import User
from app.models.role import Role, user_roles
from app.services.rate_limiter import RateLimiter
from app.core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    payload = verify_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    email = payload.get("sub")
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
        # Assuming user_roles is defined elsewhere or imported, need to check
        # For now, keeping the structure as it was but with get_current_user defined.
        # Wait, user_roles is not imported in deps.py. 
        # I need to find where user_roles is defined.
        result = await db.execute(
            select(Role).join(user_roles).where(user_roles.c.user_id == current_user.id)
        )
        user_roles_list = result.scalars().all()
        
        if not any(role.name in self.allowed_roles for role in user_roles_list):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user

class RateLimitChecker:
    def __init__(self, limit: int, window: int):
        self.limit = limit
        self.window = window
        self.limiter = RateLimiter()

    async def __call__(self, request: Request):
        client_ip = request.client.host
        if not await self.limiter.is_allowed(f"rate_limit:{client_ip}", self.limit, self.window):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests"
            )
