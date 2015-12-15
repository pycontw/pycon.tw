from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^submit/$', views.talk_proposal_create, name='talk_proposal_create'),
    url(r'^(?P<pk>\d+)/edit/$', views.talk_proposal_update, name='talk_proposal_update'),
]
