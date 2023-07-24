from datetime import date
from dateutil.parser import parse

import pandas as pd
import validators

from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand

from apps.books.models import Book, BookGenre
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Import data from an Excel file into the Book and CustomUser models."

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file.')

    def parse_genre(self, genre_str):
        genres = genre_str.split(',')
        return genres[0].strip()

    def parse_user_names(self, full_name):
        names = full_name.split()
        first_name = " ".join(names[:-1])
        last_name = names[-1]
        return first_name, last_name

    def parse_date(self, date_obj):
        if not isinstance(date_obj, date):
            try:
                return parse(str(date_obj)).date()
            except ValueError:
                self.stdout.write(self.style.WARNING(f"Invalid date format: {date_obj}. Skipping entry."))
                return None
        else:
            return date_obj

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            file_path = kwargs['file_path']
            df = pd.read_excel(file_path, parse_dates=['data'])

            for _, row in df.iterrows():
                # Extract data from each row
                title = str(row['tytuł'])
                author = str(row['autor'])
                genre = str(row['gatunek'])
                user_name = str(row['wrzucająca/y'])
                date_added = row['data']
                review = str(row['recenzja'])

                # Check if the review URL is valid
                if review and not validators.url(review):
                    self.stdout.write(self.style.WARNING(f"Invalid URL: {review}. Skipping entry."))
                    review = None

                # Parse the genre
                genre = self.parse_genre(genre)

                # Parse the user's first name and last name
                first_name, last_name = self.parse_user_names(user_name)

                # Parse the date
                date_added = self.parse_date(date_added)

                # Check if a book with the same author and title already exists
                existing_book = Book.objects.filter(
                    Q(title__iexact=title) & Q(author__iexact=author)
                    ).first()

                # If an existing book is found, skip the entry
                if existing_book:
                    self.stdout.write(self.style.WARNING(f"Book already exists: {title} by {author}. Skipping entry."))
                    continue

                # Find or create the user and genre
                user, _ = CustomUser.objects.get_or_create(
                    first_name=first_name,
                    last_name=last_name,
                    )
                genre, _ = BookGenre.objects.get_or_create(name=genre)

                # Create a new Book instance
                book = Book(
                    title=title,
                    author=author,
                    genre=genre,
                    user=user,
                    date_added=date_added,
                    review=review,
                )

                # Save the Book instance to the database
                book.save()
                self.stdout.write(self.style.SUCCESS(f'Book {title} created.'))

            self.stdout.write(self.style.SUCCESS('Data import completed.'))
