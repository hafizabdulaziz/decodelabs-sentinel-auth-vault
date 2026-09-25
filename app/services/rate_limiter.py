import time

import redis.asyncio as redis

from app.db.redis import redis_client


class RateLimiter:
    def __init__(self, redis: redis.Redis = redis_client):
        self.redis = redis

    async def is_allowed(self, key: str, limit: int, window: int) -> bool:
        now = time.time()
        window_start = now - window
        
        async with self.redis.pipeline(transaction=True) as pipe:
            # Remove old entries
            await pipe.zremrangebyscore(key, 0, window_start)
            # Add current request
            await pipe.zadd(key, {str(now): now})
            # Count remaining
            await pipe.zcard(key)
            # Set expiry
            await pipe.expire(key, window)
            results = await pipe.execute()
            
        count = results[2]
        return count <= limit
