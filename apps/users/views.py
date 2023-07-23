from django.db.models import Count
from django.shortcuts import render

from .models import CustomUser


# Create your views here.
def user_list(request):
    users = CustomUser.objects.all().annotate(book_count=Count('books'))
    context = {
        'users': users
        }
    return render(request, 'user_list.html', context)
