from django.conf.urls import url

from . import views

urlpatterns = [
    # API for CCIP
    url(r'^$', views.CCIPAPIView.as_view()),
    url(r'^sponsors/$', views.CCIPSponsorsView.as_view()),
    url(r'^staff/$', views.CCIPStaffView.as_view()),
]
