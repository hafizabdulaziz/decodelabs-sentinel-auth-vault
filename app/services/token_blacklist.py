import redis.asyncio as redis
from fastapi import Depends, HTTPException, status

from app.core.security import verify_token
from app.db.redis import get_redis


async def blacklist_token(token: str, redis_client: redis.Redis = Depends(get_redis)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        
    exp = payload.get("exp")
    if exp:
        await redis_client.setex(f"blacklist:{token}", int(exp - payload.get("iat", 0)), "true")
    else:
        await redis_client.set(f"blacklist:{token}", "true")

async def is_token_blacklisted(token: str, redis_client: redis.Redis = Depends(get_redis)):
    return await redis_client.exists(f"blacklist:{token}")
