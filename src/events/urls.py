from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^talks/$', views.TalkListView.as_view(), name='events_talk_list'),
    url(r'^talk/(?P<pk>\d+)/$', views.TalkDetailView.as_view(),
        name='events_talk_detail'),
    url(r'^talk/sponsored/(?P<slug>[-\w]+)/$',
        views.SponsoredEventDetailView.as_view(),
        name='events_sponsored_event_detail'),
    url(r'^sponsored/(?P<pk>\d+)/$',    # Kept for backward compatibility.
        views.SponsoredEventRedirectView.as_view()),
]
