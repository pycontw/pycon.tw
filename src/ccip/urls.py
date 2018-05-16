from django.conf.urls import url

from . import views

urlpatterns = [
    # API for CCIP
    url(r'^$', views.CCIPAPIView.as_view()),
]
