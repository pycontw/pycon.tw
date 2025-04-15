from django.urls import path

from proposals.api.views import (
    LLMReviewByProposalAPIView,
    LLMReviewListCreateAPIView,
    LLMReviewRetrieveUpdateDestroyAPIView,
    ProposalSummaryAPIView,
)

urlpatterns = [
    path("summary/", ProposalSummaryAPIView.as_view()),
    path("llm-reviews/", LLMReviewListCreateAPIView.as_view()),
    path("llm-reviews/<int:pk>/", LLMReviewRetrieveUpdateDestroyAPIView.as_view()),
    path("llm-reviews/proposal/<int:proposal_id>/", LLMReviewByProposalAPIView.as_view()),
]
