from django.conf.urls import url
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    url(r'^schedule/$', views.ScheduleView.as_view(), name='events_schedule'),
    url(r'^schedule/new/$', views.ScheduleCreateView.as_view()),
    url(r'^talks/$', views.TalkListView.as_view(), name='events_talk_list'),
    url(r'^talk/(?P<pk>\d+)/$', views.TalkDetailView.as_view(),
        name='events_talk_detail'),
    url(r'^talk/sponsored/(?P<slug>[-\w]+)/$',
        views.SponsoredEventDetailView.as_view(),
        name='events_sponsored_event_detail'),

    # Backward compatibility to the static events page.
    url(r'^talk/$', RedirectView.as_view(pattern_name='events_talk_list')),
]
