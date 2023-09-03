import locale

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect

from .forms import CustomUserForm
from .models import CustomUser


# Create your views here.
def user_list(request):
    # Get the sort parameter from the request
    sort_param = request.GET.get('sort', None)

    # Define default sort
    default_sort = 'book_count'

    # Define valid sorting options
    valid_sort_options = {
        'last_name': 'last_name',
        'book_count': '-book_count',
    }

    # Get the valid sort option from the request
    sort_field = valid_sort_options.get(sort_param, default_sort)

    # Get users with ordering by sort field
    users = CustomUser.objects.all().annotate(book_count=Count('books'))
    if sort_param == 'last_name':
        users = sorted(users, key=lambda u: locale.strxfrm(u.last_name))
    else:
        users = users.order_by(sort_field)

    # Define context
    context = {
        'users': users
        }

    # Return the rendered template
    return render(request, 'user_list.html', context)
