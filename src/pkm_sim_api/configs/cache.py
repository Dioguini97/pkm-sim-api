from typing import Optional

from redis.asyncio import Redis
import os


class Cache:
    redis: Optional[Redis] = None

CACHE = Cache()
async def connect_to_redis():
    CACHE.redis = Redis(
        host="redis://localhost:6379",
        port=6379,
        decode_responses=True
    )
    await CACHE.redis.ping()
    print("Redis conectado!")

async def close_redis_conn():
    if CACHE.redis:
        await CACHE.redis.close()
        print("Redis fechado!")

async def get_redis():
    return CACHE.redis


