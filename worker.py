from time import sleep
from celery import Celery
from kombu import Connection, Queue
import redis


redis_client = redis.Redis(host="localhost", port=6379, db=1)


app = Celery("app")


def enforce_priority(task):
    # step 1: if task has a {"priority": <uuid>} header, write this to a redis hash
    # instead of redis, you can use a db - as long as it supports an atomic get/delete
    if task.request.headers and task.request.headers.get("priority"):
        redis_client.hdel("priority", str(task.request.headers["priority"]))
    else:
        if redis_client.hlen("priority"):
            task.retry(countdown=2)


@app.task(bind=True, max_retries=None)
def task1(self, *args, **kwargs):
    enforce_priority(self)
    print(f"Hello from task1")
    sleep(1)


@app.task(bind=True, max_retries=None)
def task2(self, *args, **kwargs):
    enforce_priority(self)
    print(f"Hello from task2")
