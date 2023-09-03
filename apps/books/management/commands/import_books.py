from datetime import date
from dateutil.parser import parse

import pandas as pd
import validators

from django.db import transaction
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

            create_count = 0
            update_count = 0

            for _, row in df.iterrows():
                # Extract data from each row
                title = str(row['tytuł'])
                author = str(row['autor'])
                genre_name = str(row['gatunek'])
                user_name = str(row['wrzucająca/y'])
                date_added = row['data']
                review = str(row['recenzja'])

                # Check if the review URL is valid
                if review and not validators.url(review):
                    self.stdout.write(self.style.WARNING(f"Invalid URL: {review}. Skipping entry."))
                    review = None

                # Parse the genre
                genre_name = self.parse_genre(genre_name)

                # Parse the user's first name and last name
                first_name, last_name = self.parse_user_names(user_name)

                # Parse the date
                date_added = self.parse_date(date_added)

                # Find or create the user
                # Check if any users with first_name and last_name already exist
                user_duplicates = CustomUser.objects.filter(
                    first_name=first_name,
                    last_name=last_name,
                )
                # If there are duplicates, leave the first one and delete the rest
                if user_duplicates.count() > 1:
                    user_duplicates = user_duplicates[1:]
                    user_duplicates.delete()
                    self.stdout.write(
                        self.style.WARNING(
                            f"Multiple users with name {first_name} {last_name} found. Using the first one."
                            )
                        )
                    user = CustomUser.objects.get(
                        first_name=first_name,
                        last_name=last_name,
                        )

                elif user_duplicates.count() == 1:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"User {first_name} {last_name} found."
                            )
                        )
                    user = CustomUser.objects.get(
                        first_name=first_name,
                        last_name=last_name,
                        )

                else:
                    user = CustomUser(
                        first_name=first_name,
                        last_name=last_name,
                        active=True,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'New user {first_name} {last_name} created.'
                            )
                        )
                    # Save the instance to the database
                    user.save()

                # Find or create the genre
                # Check if any genres with genre_name already exist
                genre_duplicates = BookGenre.objects.filter(
                    name=genre_name,
                )
                # If there are duplicates, leave the first one and delete the rest
                if genre_duplicates.count() > 1:
                    genre_duplicates = genre_duplicates[1:]
                    genre_duplicates.delete()
                    self.stdout.write(
                        self.style.WARNING(
                            f"Multiple genres with name {genre_name} found. Using the first one."
                            )
                        )
                    genre = BookGenre.objects.get(
                        name=genre_name,
                    )
                elif genre_duplicates.count() == 1:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Genre {genre_name} found."
                            )
                        )
                    genre = BookGenre.objects.get(
                        name=genre_name,
                        )
                else:
                    genre = BookGenre(
                        name=genre_name,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'New genre {genre_name} created.'
                            )
                        )
                    # Save the instance to the database
                    genre.save()

                # Find or create the book
                # Check if any genres with genre_name already exist
                book_duplicates = Book.objects.filter(
                    title=title,
                    author=author,
                )
                # If there are duplicates, leave the first one and delete the rest
                if book_duplicates.count() > 1:
                    book_duplicates = book_duplicates[1:]
                    book_duplicates.delete()
                    self.stdout.write(
                        self.style.WARNING(
                            f"Multiple books with title {title} found. Using the first one."
                            )
                        )
                    book = Book.objects.get(
                        title=title,
                        author=author,
                        )
                    created = False
                elif book_duplicates.count() == 1:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Book {title} found."
                            )
                        )
                    book = Book.objects.get(
                        title=title,
                        author=author,
                        )
                    created = False
                else:
                    book = Book(
                        title=title,
                        author=author,
                        genre=genre,
                        user=user,
                        date_added=date_added,
                        review=review,
                    )
                    # Save the instance to the database
                    book.save()
                    created = True

                # If the book already exists, update the necessary fields
                if not created:
                    updated = False
                    if book.genre != genre:
                        book.genre = genre
                        updated = True
                    if book.user != user:
                        book.user = user
                        updated = True
                    if book.date_added != date_added:
                        book.date_added = date_added
                        updated = True
                    if book.review != review:
                        book.review = review
                        updated = True

                    if updated:
                        book.save()
                        update_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Book {title} updated. Create count: {create_count}. Update count: {update_count}."
                            )
                        )
                    continue

                create_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Book {title} created. Create count: {create_count}. Update count: {update_count}.'
                    )
                )

            self.stdout.write(self.style.SUCCESS('Data import completed.'))
            self.stdout.write(self.style.SUCCESS(f'{create_count} books created. {update_count} books updated.'))
            if user_duplicates:
                self.stdout.write(self.style.WARNING(f"Duplicate users found:\n{user_duplicates}."))
            if genre_duplicates:
                self.stdout.write(self.style.WARNING(f"Duplicate genres found:\n{genre_duplicates}."))
