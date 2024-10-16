# app/celery.py (or wherever your Celery app is defined)
from celery import Celery
from app.config import settings

def make_celery():
    celery_app = Celery(
        "tasks",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
    )

    celery_app.autodiscover_tasks(["app.tasks.extract"])

    return celery_app

celery = make_celery()
