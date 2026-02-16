import redis
from rq import Queue
from flask import current_app


def get_queue(name: str = "default") -> Queue:
    conn = redis.from_url(current_app.config["REDIS_URL"])
    return Queue(name, connection=conn)
