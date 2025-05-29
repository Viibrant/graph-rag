from upstash_redis import Redis

redis: Redis = Redis.from_env()


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
        return redis.ping() is str
    except Exception as e:
        print(f"Redis health check failed: {e}")
        return False
