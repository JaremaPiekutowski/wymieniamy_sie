import pandas as pd
from django.core.management.base import BaseCommand
from apps.books.models import Book


class Command(BaseCommand):
    help = "Delete duplicate books from the database, keeping only those listed in an Excel file."

    def handle(self, *args, **kwargs):
        # Read the Excel file into a DataFrame
        df = pd.read_excel('data/data_non_duplicated.xlsx')

        for index, row in df.iterrows():
            title = row['title']
            author = row['author']

            # Find the book in the database with the same title and author as in the Excel file
            book_to_keep = Book.objects.filter(title=title, author=author).first()

            if book_to_keep:
                # Find all books in the database with the same title but different authors
                books_to_delete = Book.objects.filter(title=title).exclude(id=book_to_keep.id)

                # Delete those books
                books_to_delete.delete()

                deleted_books = ','.join([book.title for book in books_to_delete])
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted books: {deleted_books}'))

                self.stdout.write(self.style.SUCCESS(f'Successfully kept book: {title} by {author}'))
            else:
                self.stdout.write(self.style.WARNING(f'Book not found in database: {title} by {author}'))
