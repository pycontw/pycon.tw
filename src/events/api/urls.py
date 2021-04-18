from django.urls import path

from events import api

app_name = 'app'

urlpatterns = [
    path('talkproposal/<int:pk>', api.TalkDetailAPIView.as_view()),
]
