from datetime import datetime

import pandas as pd
import validators
from django.core.management.base import BaseCommand

from apps.books.models import Book, BookGenre
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Import data from an Excel file into the Book and CustomUser models."

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file.')

    def parse_user_names(self, full_name):
        names = full_name.split()
        first_name = " ".join(names[:-1])
        last_name = names[-1]
        return first_name, last_name

    def parse_genre(self, genre_str):
        genres = genre_str.split(',')
        return genres[0].strip()

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            # Extract data from each row
            title = str(row['tytuł'])
            author = str(row['autor'])
            genre = str(row['gatunek'])
            user_name = str(row['wrzucająca/y'])
            date_added = row['data']
            review = str(row['recenzja'])

            # Parse the date
            if not isinstance(date_added, datetime):
                try:
                    date_added = datetime.strptime(str(date_added), '%d.%m.%Y').date()
                except ValueError:
                    self.stdout.write(self.style.WARNING(f"Invalid date format: {date_added}. Skipping entry."))
                    date_added = None

            # Check if the review URL is valid
            if review and not validators.url(review):
                self.stdout.write(self.style.WARNING(f"Invalid URL: {review}. Skipping entry."))
                review = None

            # Parse the user's first name and last name
            first_name, last_name = self.parse_user_names(user_name)

            # Parse the genre
            genre = self.parse_genre(genre)

            # Check if a book with the same author and title already exists
            existing_book = Book.objects.filter(
                author=author,
                title=title
                ).first()

            if existing_book:
                self.stdout.write(self.style.WARNING(f"Book '{title}' by {author} already exists. Skipping entry."))
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
