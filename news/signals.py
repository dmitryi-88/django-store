from django.core.cache import caches
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .cache_utils import invalidate_news_cache
from .models import News


@receiver(post_save, sender=News)
@receiver(post_delete, sender=News)
def clear_news_cache(sender, **kwargs):
    invalidate_news_cache()
    caches["pages"].clear()
