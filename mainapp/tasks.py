from datetime import timedelta
from celery import shared_task
from django.contrib.auth import get_user_model as user
from django.utils.timezone import now
import logging

@shared_task
def delete_inactive_users():
    logging.info("Deleting inactive users")
    time_threshold = now() - timedelta(days=365)
    user().objects.filter(last_login__lte=time_threshold).exclude(is_staff=True).delete()