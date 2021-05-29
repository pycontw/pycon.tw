from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('talk/<int:pk>', views.TalkDetailAPIView.as_view()),
    path('tutorial/<int:pk>', views.TutorialDetailAPIView.as_view()),
    path('tutorials/', views.TutorialListAPIView.as_view()),
    path('schedule/', views.ScheduleAPIView.as_view()),
]
