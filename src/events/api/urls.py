from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('talk/<int:pk>', views.TalkDetailAPIView.as_view()),
]
