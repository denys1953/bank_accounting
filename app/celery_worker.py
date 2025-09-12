from celery import Celery

redis_url = "redis://localhost:6379/0"

celery_app = Celery(
    __name__,
    broker=redis_url,
    backend=redis_url 
)

# Опціональні налаштування
celery_app.conf.update(
    task_track_started=True,
)