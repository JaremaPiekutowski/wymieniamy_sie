import locale

from datetime import date
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Count, Case, When, Value, IntegerField
from django.shortcuts import render, redirect

from .models import CustomUser


# Create your views here.
def user_list(request):
    # Get the sort parameter from the request
    sort_param = request.GET.get('sort', None)

    # Define default sort
    default_sort = '-book_count'

    # Define valid sorting options
    valid_sort_options = {
        'last_name': 'last_name',
        'book_count': '-book_count',
    }

    # Get the valid sort option from the request
    sort_field = valid_sort_options.get(sort_param, default_sort)

    # Get the current date
    current_date = date.today()
    current_year = current_date.year
    next_year = current_year + 1

    # Determine the date range for the current half-year
    if current_date.month <= 6:
        start_date = date(current_date.year, 1, 1)
        end_date = date(current_date.year, 7, 1)
    else:
        start_date = date(current_date.year, 7, 1)
        end_date = date(next_year, 1, 1)

    # Get users with ordering by sort field
    users = CustomUser.objects.filter(active=True).annotate(
        book_count=Count('books'),
        books_this_half_year=Count(
            Case(
                When(books__date_added__range=(start_date, end_date), then=1),
                output_field=IntegerField(),
            )
        ),
        books_needed=Case(
            When(books_this_half_year__gte=2, then=Value(0)),
            When(books_this_half_year=1, then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
            )
        )
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


class SiteWideLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


def site_wide_login(request):
    if request.method == 'POST':
        form = SiteWideLoginForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == settings.SITE_WIDE_PASSWORD:
                request.session['authenticated'] = True
                return redirect('/')
            else:
                return HttpResponse("Unauthorized", status=401)
    else:
        form = SiteWideLoginForm()
    return render(request, 'site_wide_login.html', {'form': form})
