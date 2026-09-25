from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.redis import redis_client
from app.services.token_blacklist import is_token_blacklisted


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/v1/users/"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing or invalid token",
                )
            token = auth_header.replace("Bearer ", "")
            if await is_token_blacklisted(token, redis_client):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked",
                )
        
        response = await call_next(request)
        return response
