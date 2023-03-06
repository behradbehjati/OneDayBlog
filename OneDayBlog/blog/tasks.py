from celery import shared_task
from .models import Article
import time
from datetime import datetime, timedelta
@shared_task
def delete(id):
    time.sleep(60*60*24)
    Article.objects.get(id=id).delete()
    one_day_ago = datetime.now() - timedelta(days=1)
    Article.objects.filter(publish_date__lt=one_day_ago).delete()
    return True
