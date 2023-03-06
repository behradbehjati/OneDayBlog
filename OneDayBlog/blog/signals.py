from django.db.models.signals import post_save

from django.dispatch import receiver
from .models import Article
from .tasks import delete
@receiver(post_save, sender=Article)
def create_article(sender, instance, created, **kwargs):

    if created:
        delete.delay(instance.id)
