from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^submit/$', views.proposal_create, name='proposal_create'),
    url(r'^(?P<pk>\d+)/edit/$', views.proposal_update, name='proposal_update'),
]
