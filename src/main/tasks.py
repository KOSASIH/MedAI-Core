# src/main/tasks.py

from celery import Celery

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, result_backend=Config.CELERY_RESULT_BACKEND)

@celery.task
def send_welcome_email(email):
    # Send welcome email using email service
    pass
