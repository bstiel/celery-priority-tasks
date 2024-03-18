import os
import time
import logging
from uuid import uuid4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from worker import task1, task2, redis_client


def main():
    for _ in range(3):
        task1.s().apply_async()

    task_id = task2.s().apply_async(headers={"priority": True})
    redis_client.hset("priority", str(task_id), "True")


if __name__ == "__main__":
    main()
