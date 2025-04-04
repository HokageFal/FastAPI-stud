import os
import time

from celery import Celery

BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://:9898@redis:6379/0")
RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://:9898@redis:6379/0")

celery = Celery(__name__, broker=BROKER_URL, backend=RESULT_BACKEND)


@celery.task
def create_channel_celery(a, b):
    return a + b

celery.conf.broker_connection_retry_on_startup = True