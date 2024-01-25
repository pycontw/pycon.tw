from django.conf.urls import url
from django.views.generic import RedirectView

from events import views

urlpatterns = [
    url(r'^talks/$', views.TalkListView.as_view(),
        name='events_talk_list'),
    url(r'^tutorials/$', views.TutorialListView.as_view(),
        name='events_tutorial_list'),

    url(r'^talk/(?P<pk>\d+)/$', views.TalkDetailView.as_view(),
        name='events_talk_detail'),
    url(r'^talk/sponsored/(?P<slug>[-\w]+)/$',
        views.SponsoredEventDetailView.as_view(),
        name='events_sponsored_event_detail'),
    url(r'^tutorial/(?P<pk>\d+)/$', views.TutorialDetailView.as_view(),
        name='events_tutorial_detail'),

    # Backward compatibility to the static events page.
    url(r'^talk/$', RedirectView.as_view(pattern_name='events_talk_list')),
]
