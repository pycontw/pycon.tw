from django.urls import path

from proposals.api.views import ProposalSummaryAPIView

urlpatterns = [
    path("summary/", ProposalSummaryAPIView.as_view()),
]
