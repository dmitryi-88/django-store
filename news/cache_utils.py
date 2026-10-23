from django.core.cache import cache
from django.db.models import Count

from .models import Category

CACHE_TIMEOUT = 300


def get_cached_categories():
    key = "news:categories"

    categories = cache.get(key)

    if categories is None:
        categories = list(Category.objects.all())
        cache.set(key, categories, CACHE_TIMEOUT)

    return categories


def get_cached_category_news_count():
    key = "news:category_news_count"

    counts = cache.get(key)

    if counts is None:
        counts = dict(
            Category.objects.annotate(news_count=Count("news")).values_list(
                "id", "news_count"
            )
        )
        cache.set(key, counts, CACHE_TIMEOUT)

    return counts


def get_cached_categories_with_counts():
    key = "news:categories_with_counts"
    result = cache.get(key)

    if result is None:
        result = list(
            Category.objects.annotate(news_count=Count("news")).values(
                "id", "name", "news_count"
            )
        )
        cache.set(key, result, CACHE_TIMEOUT)

    return result


def invalidate_news_cache():
    cache.delete("news:categories")
    cache.delete("news:category_news_counts")
    cache.delete("news:categories_with_counts")