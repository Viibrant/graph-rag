import os

from dotenv import load_dotenv
from upstash_redis import Redis

load_dotenv()

redis: "Redis"

if os.getenv("UPSTASH_REDIS_REST_URL") and os.getenv("UPSTASH_REDIS_REST_TOKEN"):
    # Upstash (serverless, HTTP)
    from upstash_redis import Redis

    redis = Redis.from_env()
elif os.getenv("REDIS_URL"):
    # Local Redis (docker-compose, TCP)
    import redis as redis_py

    redis = redis_py.Redis.from_url(os.environ["REDIS_URL"])
else:
    raise RuntimeError("No Redis configuration found. Set REDIS_URL or UPSTASH_REDIS_*")


def get_redis_conn() -> Redis:
    global redis
    return redis


def is_redis_healthy() -> bool:
    """
    Check if the Redis connection is healthy.

    Returns:
        bool: True if the Redis connection is healthy, False otherwise.
    """
    try:
        return bool(redis.ping())
    except Exception as e:
        print(f"Redis health check failed: {e}")
        return False
