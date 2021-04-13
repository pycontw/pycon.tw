from django.urls import path
from sponsors.api.views import SponsorAPIView, JobAPIView

urlpatterns = [
    path("", SponsorAPIView.as_view()),
    path("jobs/", JobAPIView.as_view()),
]
