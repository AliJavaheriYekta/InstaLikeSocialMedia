from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from contents.models import Story


@shared_task
def remove_expired_stories():
    threshold_time = timezone.now() - timedelta(hours=24)
    Story.objects.filter(created_at__lt=threshold_time).delete()
