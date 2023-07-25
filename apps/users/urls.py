from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('add_user/', views.add_custom_user, name='add_user'),
]
