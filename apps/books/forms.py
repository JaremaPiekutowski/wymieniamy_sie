from django import forms
from django.db.models import Func
from django.core.cache import cache
from .models import BookGenre

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

        # Cache form choices to avoid repeated database queries
        cache_key_users = 'book_form_users'
        cache_key_genres = 'book_form_genres'

        # Get users from cache or database
        users_choices = cache.get(cache_key_users)
        if users_choices is None:
            users = CustomUser.objects.filter(active=True).order_by('last_name', 'first_name')
            users_choices = [("", "Wybierz")] + [(u.id, f"{u.first_name} {u.last_name}") for u in users]
            cache.set(cache_key_users, users_choices, 300)  # Cache for 5 minutes
        self.fields['user'].choices = users_choices

        # Get genres from cache or database
        genres_choices = cache.get(cache_key_genres)
        if genres_choices is None:
            genres = BookGenre.objects.all().order_by('name')
            genres_choices = [("", "Wybierz")] + [(g.id, g.name) for g in genres]
            cache.set(cache_key_genres, genres_choices, 300)  # Cache for 5 minutes
        self.fields['genre'].choices = genres_choices


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

        # Cache form choices to avoid repeated database queries
        cache_key_users = 'book_search_form_users'
        cache_key_genres = 'book_search_form_genres'

        # Get users from cache or database
        users_choices = cache.get(cache_key_users)
        if users_choices is None:
            users = CustomUser.objects.filter(active=True).order_by('last_name', 'first_name')
            users_choices = [("", "Wybierz")] + [(u.id, f"{u.first_name} {u.last_name}") for u in users]
            cache.set(cache_key_users, users_choices, 300)  # Cache for 5 minutes
        self.fields['user'].choices = users_choices

        # Get genres from cache or database
        genres_choices = cache.get(cache_key_genres)
        if genres_choices is None:
            genres = BookGenre.objects.all().order_by('name')
            genres_choices = [("", "Wybierz")] + [(g.id, g.name) for g in genres]
            cache.set(cache_key_genres, genres_choices, 300)  # Cache for 5 minutes
        self.fields['genre'].choices = genres_choices
