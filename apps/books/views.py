import datetime
import locale

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q, Case, When, Value, BooleanField
from django.shortcuts import render, redirect

from .models import Book, BookGenre
from ..users.models import CustomUser
from .forms import BookForm, BookSearchForm


# Create your views here.
def homepage(request):
    today = datetime.date.today()
    current_month = today.month
    current_year = today.year
    if current_month <= 6:
        start_date = datetime.datetime(current_year, 1, 1)
        end_date = datetime.datetime(current_year, 6, 30)
    else:
        start_date = datetime.datetime(current_year, 7, 1)
        end_date = datetime.datetime(current_year, 12, 31)

    formatted_start_date = start_date.strftime('%d.%m')
    formatted_end_date = end_date.strftime('%d.%m.%y')

    # Filter only books whose date_added is not none and order by date added descending and get first 5
    last_submitted_books = Book.objects.exclude(date_added__isnull=True).order_by('-date_added')[:5]

    active_users = CustomUser.objects.filter(active=True)

    users_with_no_books = active_users.exclude(
        books__date_added__gte=start_date
        ).order_by('last_name', 'first_name')

    users_with_most_books = active_users.annotate(
        book_count=Count('books', filter=Q(
            books__date_added__gte=start_date
            ))
        ).order_by('-book_count')[:5]

    context = {
        'start_date': formatted_start_date,
        'end_date': formatted_end_date,
        'last_submitted_books': last_submitted_books,
        'users_with_no_books': users_with_no_books,
        'users_with_most_books': users_with_most_books,
    }

    return render(request, 'homepage.html', context)


def book_list(request):
    sort_param = request.GET.get('sort', 'title')

    if sort_param == 'date_added':
        books = Book.objects.annotate(
            is_date_added_null=Case(
                When(date_added__isnull=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).order_by('is_date_added_null', '-date_added')
    else:
        books = Book.objects.all()

        if sort_param in ['author', 'title']:
            books = sorted(books, key=lambda b: locale.strxfrm(getattr(b, sort_param)))
        elif sort_param == 'user__last_name':
            books = sorted(books, key=lambda b: locale.strxfrm(b.user.last_name) if b.user else '')
        elif sort_param == 'user__first_name':
            books = sorted(books, key=lambda b: locale.strxfrm(b.user.first_name) if b.user else '')
        else:
            books = books.order_by(sort_param)

    paginator = Paginator(books, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sort_param': sort_param,
    }
    return render(request, 'book_list.html', context)


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            genre = form.cleaned_data['genre']
            user = form.cleaned_data['user']
            review = form.cleaned_data['review']
            # Get genre object
            if genre and genre != "Wybierz":
                genre = BookGenre.objects.get(name=genre)
            else:
                genre = None
            if user and user != "Wybierz":
                user = CustomUser.objects.get(id=user)
            else:
                messages.error(request, f"Nie wybrano użytkownika.")
                return redirect('add_book')
            # See if no book of the same author and title exists
            if Book.objects.filter(title=title, author=author).exists():
                messages.error(request, f"Książka {title} {author} już istnieje.")
                return redirect('add_book')
            else:
                book = Book(
                    title=title,
                    author=author,
                    genre=genre,
                    user=user,
                    review=review,
                )
                book.save()
                messages.success(request, f"Książka {title} {author} została dodana.")
                return redirect('book_list')

    else:
        form = BookForm()

    context = {
        'form': form,
    }
    return render(request, 'add_book.html', context)


def book_search(request):
    books = Book.objects.none()

    # Add search functionality for Book model
    form = BookSearchForm(request.GET or None)
    if form.is_valid():
        title = form.cleaned_data['title']
        author = form.cleaned_data['author']
        genre = form.cleaned_data['genre']
        user = form.cleaned_data['user']

        books = Book.objects.all()
        print(title, author, genre, user)
        if title:
            books = books.filter(title__icontains=title)
        if author:
            books = books.filter(author__icontains=author)
        if genre:
            books = books.filter(genre=genre)
        if user:
            books = books.filter(user=user)
        if genre == "Wybierz" and user == "Wybierz" and not title and not author:
            books = Book.objects.none()
        if not genre and not user and not title and not author:
            books = Book.objects.none()

    sort_param = request.GET.get('sort', 'title')
    if sort_param == 'date_added':
        books = books.annotate(
            is_date_added_null=Case(
                When(date_added__isnull=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).order_by('is_date_added_null', '-date_added')
    else:
        books = books.order_by(sort_param)

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'sort_param': sort_param,
        }
    return render(
        request,
        'search_book.html',
        context
        )
