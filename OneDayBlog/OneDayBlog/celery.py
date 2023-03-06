import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','OneDayBlog.settings')
app=Celery('OneDayBlog')
app.config_from_object('django.conf:settings',namespace='Celery')