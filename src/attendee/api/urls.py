from django.urls import path

from attendee.api.views import AttendeeAPIView


urlpatterns = [
    path('verify/', AttendeeAPIView.as_view()),
]
