from django.conf.urls import url

from . import views
from ext2020 import views as ext2020_views

urlpatterns = [
    # API for CCIP
    url(r'^$', views.CCIPAPIView.as_view()),
    url(r'^sponsors/$', views.CCIPSponsorsView.as_view()),
    url(r'^staff/$', views.CCIPStaffView.as_view()),
    url(r'^live/$', ext2020_views.LiveBroadcastView.as_view(template_name='ccip/live.html')),
    url(r'^discord/$', ext2020_views.DiscordView.as_view(template_name='ccip/discord.html')),
    url(r'^community-track/$', ext2020_views.CommunityTrackView.as_view(template_name='ccip/community_track.html')),
]
