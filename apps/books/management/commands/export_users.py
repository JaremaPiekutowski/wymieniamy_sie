from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = 'Lists users with books added later than six months ago'

    def handle(self, *args, **kwargs):
        six_months_ago = timezone.now() - timedelta(days=180)

        users_with_books = CustomUser.objects.filter(
            books__date_added__gte=six_months_ago
        )

        with open('users_books.txt', 'w', encoding='utf-8') as file:
            for user in users_with_books:
                books = user.books.filter(date_added__gte=six_months_ago)
                for book in books:
                    file.write(f'User ID: {user.id}, Book: "{book.title}", Date Added: {book.date_added}\n')
