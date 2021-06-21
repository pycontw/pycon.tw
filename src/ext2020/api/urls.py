from django.urls import path

from ext2020.api.views import AttendeeAPIView


urlpatterns = [
    path('verify/', AttendeeAPIView.as_view()),
]
