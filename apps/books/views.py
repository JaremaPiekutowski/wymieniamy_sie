from django.shortcuts import render

from .models import Book


# Create your views here.
def homepage(request):
    last_submitted_books = Book.objects.all().order_by('-date_added')[:3]
    context = {
        'last_submitted_books': last_submitted_books
        }

    return render(request, 'homepage.html', context)


def book_list(request):
    sort_param = request.GET.get('sort', 'title')
    books = Book.objects.all().order_by(sort_param)
    context = {
        'books': books
        }
    return render(request, 'book_list.html', context)
