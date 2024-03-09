import locale

from django import forms
from django.db.models import Func
from .models import Book, BookGenre

from apps.users.models import CustomUser


class StrXfrm(Func):
    function = 'STRXFRM'
    template = '%(function)s(%(expressions)s)'


class BookForm(forms.Form):
    title = forms.CharField(required=True)
    author = forms.CharField(required=False)
    genre = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices=[],  # Initial empty choices
    )
    user = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=[],  # Initial empty choices
    )
    review = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sort users and set choices manually
        users = CustomUser.objects.filter(active=True)
        users_sorted = sorted(users, key=lambda u: locale.strxfrm(u.last_name))
        self.fields['user'].choices = [("", "Wybierz")]+[(u.id, u.first_name+" "+u.last_name) for u in users_sorted]

        # Sort genres and set choices manually
        genres = BookGenre.objects.all()
        genres_sorted = sorted(genres, key=lambda g: locale.strxfrm(g.name))
        self.fields['genre'].choices = [("", "Wybierz")]+[(g.id, g.name) for g in genres_sorted]


class BookSearchForm(forms.Form):
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)
    genre = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices=[],  # Initial empty choices
    )
    user = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices=[],  # Initial empty choices
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sort users and set choices manually
        users = CustomUser.objects.filter(active=True)
        users_sorted = sorted(users, key=lambda u: locale.strxfrm(u.last_name))
        self.fields['user'].choices = [("", "Wybierz")]+[(u.id, u.first_name+" "+u.last_name) for u in users_sorted]

        # Sort genres and set choices manually
        genres = BookGenre.objects.all()
        genres_sorted = sorted(genres, key=lambda g: locale.strxfrm(g.name))
        self.fields['genre'].choices = [("", "Wybierz")]+[(g.id, g.name) for g in genres_sorted]
