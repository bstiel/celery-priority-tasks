producer: watchfiles --filter python 'python producer.py' .
worker: watchfiles --filter python 'celery --app=worker.app worker --pool=solo --concurrency=2 --loglevel=INFO' .