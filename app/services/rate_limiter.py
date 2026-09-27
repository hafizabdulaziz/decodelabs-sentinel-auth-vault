import time

import redis.asyncio as redis

from app.db.redis import redis_client


class RateLimiter:
    def __init__(self, redis: redis.Redis = redis_client):
        self.redis = redis
        self.memory_store = {}

    async def is_allowed(self, key: str, limit: int, window: int) -> bool:
        now = time.time()
        window_start = now - window
        try:
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
        except Exception:
            # Fallback to in-memory rate limiting if Redis is offline
            if key not in self.memory_store:
                self.memory_store[key] = []
            self.memory_store[key] = [t for t in self.memory_store[key] if t > window_start]
            self.memory_store[key].append(now)
            count = len(self.memory_store[key])
            return count <= limit
