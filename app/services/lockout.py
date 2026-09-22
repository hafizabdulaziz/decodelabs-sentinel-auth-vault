import redis.asyncio as redis
from app.db.redis import redis_client

class LockoutService:
    def __init__(self, redis: redis.Redis = redis_client):
        self.redis = redis

    async def register_failed_attempt(self, identifier: str):
        key = f"failed_attempts:{identifier}"
        await self.redis.incr(key)
        await self.redis.expire(key, 3600)  # 1 hour lockout window

    async def is_locked(self, identifier: str) -> bool:
        key = f"failed_attempts:{identifier}"
        attempts = await self.redis.get(key)
        return attempts and int(attempts) >= 5

    async def reset_attempts(self, identifier: str):
        await self.redis.delete(f"failed_attempts:{identifier}")
