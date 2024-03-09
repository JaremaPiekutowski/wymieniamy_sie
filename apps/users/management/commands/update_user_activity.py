import pandas as pd

from django.db import transaction
from django.core.management.base import BaseCommand

from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Make active users (from xls) active and all other users inactive."

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file.')

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            file_path = kwargs['file_path']
            try:
                df = pd.read_excel(file_path)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to read Excel file: {e}"))
                return

            user_count = 1

            for user in CustomUser.objects.all():
                user_count += 1
                user.active = False
                user_full_name = user.first_name + " " + user.last_name
                if user_full_name in df['full_name'].values.tolist():
                    user.active = True
                else:
                    user.active = False
                    print(f"{user_count}. User {user_full_name} is inactive.")
                user.save(update_fields=['active'])
            self.stdout.write(
                self.style.SUCCESS(
                    'User data update completed.'
                    )
                )
