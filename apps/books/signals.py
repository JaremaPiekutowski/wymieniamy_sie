from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import BookGenre
from apps.users.models import CustomUser


@receiver([post_save, post_delete], sender=CustomUser)
def clear_user_cache(sender, instance, **kwargs):
    """Clear form caches when users are modified"""
    cache_keys = [
        'book_form_users',
        'book_search_form_users',
    ]
    for key in cache_keys:
        cache.delete(key)


@receiver([post_save, post_delete], sender=BookGenre)
def clear_genre_cache(sender, instance, **kwargs):
    """Clear form caches when genres are modified"""
    cache_keys = [
        'book_form_genres',
        'book_search_form_genres',
    ]
    for key in cache_keys:
        cache.delete(key)
