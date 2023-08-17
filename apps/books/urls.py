from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('books/', views.book_list, name='book_list'),
    path('books/search', views.book_search, name='book_search'),
    path('add_book/', views.add_book, name='add_book'),
]
