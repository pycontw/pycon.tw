from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('talk/<int:pk>/', views.TalkDetailAPIView.as_view()),
    path('talks/', views.TalkListAPIView.as_view()),
    path('sponsors-event/', views.SponsoredEventListAPIView.as_view()),
    path('talk/<int:pk>', views.TalkDetailAPIView.as_view()),
    path('tutorial/<int:pk>', views.TutorialDetailAPIView.as_view()),
    path('tutorials/', views.TutorialListAPIView.as_view()),
    path('schedule/', views.ScheduleAPIView.as_view()),
    path('keynotes/', views.KeynoteEventListAPIView.as_view()),
]
