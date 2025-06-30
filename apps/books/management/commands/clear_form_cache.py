from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Clear form choice caches for books app'

    def handle(self, *args, **options):
        cache_keys = [
            'book_form_users',
            'book_form_genres',
            'book_search_form_users',
            'book_search_form_genres',
        ]

        for key in cache_keys:
            cache.delete(key)

        self.stdout.write(
            self.style.SUCCESS('Successfully cleared form caches')
        )