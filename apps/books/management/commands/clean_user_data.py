from django.core.management.base import BaseCommand
from apps.books.models import Book
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Change incorrect names."

    def handle(self, *args, **kwargs):
        changes = {
            ('Kinga', 'Zglinicka'): ('Kinga', 'Benevides'),
            ('Ania', 'Ły'): ('Ania', 'Łobacz'),
            ('Basia', 'Szymańska'): ('Barbara', 'Szymańska'),
            ('Drozd', 'Małgorzata'): ('Małgorzata', 'Drozd'),
        }

        for change in changes:
            old_first_name, old_last_name = change
            new_first_name, new_last_name = changes[change]
            old_user = CustomUser.objects.filter(first_name=old_first_name, last_name=old_last_name).first()
            if not old_user:
                self.stdout.write(self.style.WARNING(f'User not found: {old_first_name} {old_last_name}'))
                continue
            new_user = CustomUser.objects.filter(first_name=new_first_name, last_name=new_last_name).first()
            if not new_user:
                self.stdout.write(self.style.WARNING(f'User not found: {new_first_name} {new_last_name}'))
                continue
            books = Book.objects.filter(user__first_name=old_first_name, user__last_name=old_last_name)
            for book in books:
                book.user = new_user
                self.stdout.write(self.style.SUCCESS(f'Changed user for book: {book.title}'))
                book.save()
            old_user.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted user: {old_first_name} {old_last_name}'))
