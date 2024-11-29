from django.core.management.base import BaseCommand
from django.db.models import Count
from apps.books.models import Book


class Command(BaseCommand):
    help = "Delete duplicate books from the database, keeping only those listed in an Excel file."

    def handle(self, *args, **kwargs):
        books = Book.objects.all()
        duplicates = books.values('title').annotate(count=Count('title')).filter(count__gt=1)
        for duplicate in duplicates:
            print(duplicate['title'])
