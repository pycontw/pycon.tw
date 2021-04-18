from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from events import api

app_name = 'app'


router = DefaultRouter()
router.register(r'talkproposal', api.TalkProposalViewSet)  # Allow: GET, POST, HEAD, OPTIONS


urlpatterns = [
    path('', include(router.urls)),
]
