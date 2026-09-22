from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.user import User
from app.models.role import Role
from app.services.rate_limiter import RateLimiter

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
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
