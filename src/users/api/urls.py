from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
]
