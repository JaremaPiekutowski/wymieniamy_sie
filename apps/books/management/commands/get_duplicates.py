from django.db.models import Count
from django.core.management.base import BaseCommand

from apps.books.models import Book


class Command(BaseCommand):
    help = "Get book duplicates by title."

    def handle(self, *args, **kwargs):
        duplicates = Book.objects.values('title') \
            .annotate(title_count=Count('title')).filter(title_count__gt=1)
        for duplicate in duplicates:
            print(f"Title: {duplicate['title']}, Count: {duplicate['title_count']}")
