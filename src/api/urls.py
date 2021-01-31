from django.conf.urls import url

from sponsors.views import SponsorAPIView, JobAPIView

urlpatterns = [
    url(r'^sponsors/$', SponsorAPIView.as_view()),
    url(r'^jobs/$', JobAPIView.as_view()),
]
