from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sponsors/$', views.SponsorAPIView.as_view()),
    url(r'^jobs/$', views.JobAPIView.as_view()),
]
