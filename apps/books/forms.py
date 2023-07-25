from django import forms
from .models import Book, BookGenre

from apps.users.models import CustomUser


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'genre',
            'user',
            'review',
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['genre'].queryset = BookGenre.objects.order_by('name')
        self.fields['user'].queryset = CustomUser.objects.order_by('last_name')
