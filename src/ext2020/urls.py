from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^live/$', views.LiveBroadcastView.as_view(), name='live'),
    url(r'^discord/$', views.DiscordView.as_view(), name='discord'),
]
