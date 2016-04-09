from django.conf.urls import url

from .views import SponsorListView

urlpatterns = [
    url(r'^$', SponsorListView.as_view(), name='sponsor_list'),
]
