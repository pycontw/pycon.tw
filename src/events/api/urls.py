from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('schedule/', views.ScheduleAPIView.as_view()),
    path('keynotes/', views.KeynoteEventListAPIView.as_view()),
    path('speeches/', views.SpeechListAPIView.as_view()),
    path('speeches/<str:event_type>/<int:pk>/', views.SpeechDetailAPIView.as_view()),
    path('speeches/category/<str:category>', views.SpeechListByCategoryAPIView.as_view(), name="speeches-category"),
]
