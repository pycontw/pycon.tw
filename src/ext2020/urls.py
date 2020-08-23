from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^live$', views.live, name='live'),
]
