from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.user import User
from app.models.role import Role

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
