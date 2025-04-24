from upstash_redis import Redis

redis = Redis.from_env()


def get_redis_conn() -> Redis:
    global redis
    return redis
