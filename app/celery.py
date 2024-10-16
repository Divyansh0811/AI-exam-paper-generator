from celery import Celery
from app.config import settings

# Configure Celery app
celery_app = Celery(
    "app",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

# Configure Celery settings
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Auto-discover tasks in the 'tasks' module
celery_app.autodiscover_tasks(['app.tasks.extract'])
