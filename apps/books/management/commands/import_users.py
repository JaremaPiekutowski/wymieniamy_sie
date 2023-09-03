import pandas as pd

from django.db import transaction
from django.core.management.base import BaseCommand

from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Import data from an Excel file into the CustomUser models."

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

            create_count = 0
            update_count = 0

            for _, row in df.iterrows():
                # Extract data from each row
                first_name = str(row['first_name'])
                last_name = str(row['last_name'])
                active = row['active']

                # Find or create the user
                try:
                    # Check if any users with first_name and last_name already exist
                    user_duplicates = CustomUser.objects.filter(
                        first_name=first_name,
                        last_name=last_name,
                    )
                    # If there are duplicates, leave the first one and delete the rest
                    if user_duplicates.count() > 1:
                        user_duplicates = user_duplicates[1:]
                        user_duplicates.delete()
                    # Get the first user with first_name and last_name
                    user = CustomUser.objects.get(
                        first_name=first_name,
                        last_name=last_name,
                        )
                    user.active = active
                    user.save()
                    update_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"User {first_name} {last_name} updated. Created: {create_count}, updated: {update_count}."
                            )
                        )
                    continue
                except CustomUser.DoesNotExist:
                    user = CustomUser(
                        first_name=first_name,
                        last_name=last_name,
                        active=active,
                    )

                # Save the CustomUser instance to the database
                user.save()
                create_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'User {first_name} {last_name} created. Created: {create_count}, updated: {update_count}.'
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Data import completed. {create_count} users created, {update_count} users updated.'
                    )
                )
            self.stdout.write(self.style.WARNING(f"User duplicates found:\n{user_duplicates}."))
