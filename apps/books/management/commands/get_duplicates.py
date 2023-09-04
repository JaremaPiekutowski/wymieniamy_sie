import pandas as pd

from django.db.models import Count
from django.core.management.base import BaseCommand

from apps.books.models import Book


class Command(BaseCommand):
    help = "Get book duplicates by title."

    def handle(self, *args, **kwargs):
        # Create an empty list to store duplicate rows
        duplicate_rows = []

        # Group by 'title' and annotate the count
        duplicates = Book.objects.values('title').annotate(title_count=Count('title')).filter(title_count__gt=1)
        print(duplicates)
        for duplicate in duplicates:
            # Append new row with duplicate title and author
            new_row = {'title': duplicate['title']}
            duplicate_rows.append(new_row)

        # Create a DataFrame from the list of duplicate rows
        df = pd.DataFrame(duplicate_rows)

        # Save the DataFrame to an Excel file
        df.to_excel('duplicates.xlsx', index=False)
