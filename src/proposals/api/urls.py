from django.urls import path
from proposals.api.views import ProposalAPIView

urlpatterns = [
    path("summary/", ProposalAPIView.as_view()),
]
