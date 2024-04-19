import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialMedia.settings')
app = Celery('SocialMedia')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'remove_expired_stories': {
        'task': 'contents.tasks.remove_expired_stories',
        'schedule': crontab(minute='*/1'),
    },
}
