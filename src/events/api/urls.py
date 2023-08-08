from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('schedule/', views.ScheduleAPIView.as_view(), name="schedule-list"),
    path('keynotes/', views.KeynoteEventListAPIView.as_view(), name="keynotes-list"),
    path('speeches/', views.SpeechListAPIView.as_view(), name="speeches-list"),
    path('speeches/<str:event_type>/<int:pk>/', views.SpeechDetailAPIView.as_view(), name="speeches-event_type"),
    path('speeches/category/<str:category>', views.SpeechListByCategoryAPIView.as_view(), name="speeches-category"),
]
