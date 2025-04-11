from rest_framework import generics, status, views
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentication import TokenAuthentication
from proposals.api.serializers import LLMReviewSerializer
from proposals.models import LLMReview, TalkProposal, TutorialProposal
from reviews.models import Review


class ProposalSummaryAPIView(views.APIView):

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        num_proposed_talk = TalkProposal.objects.filter(cancelled=False).count()
        num_proposed_tutorial = TutorialProposal.objects.filter(cancelled=False).count()
        num_stage_1_reviews = Review.objects.filter(stage=1).count()
        num_stage_2_reviews = Review.objects.filter(stage=2).count()

        response_data = {
            "num_proposed_talk": num_proposed_talk,
            "num_proposed_tutorial": num_proposed_tutorial,
            "num_stage_1_reviews": num_stage_1_reviews,
            "num_stage_2_reviews": num_stage_2_reviews,
        }

        return Response(response_data)


class LLMReviewListCreateAPIView(generics.ListCreateAPIView):
    """API view to list all LLM reviews or create a new one."""
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LLMReviewSerializer
    queryset = LLMReview.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class LLMReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update or delete a specific LLM review."""
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LLMReviewSerializer
    queryset = LLMReview.objects.all()


class LLMReviewByProposalAPIView(APIView):
    """API view to get LLM review for a specific proposal."""
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, proposal_id):
        try:
            review = LLMReview.objects.get(proposal_id=proposal_id)
            serializer = LLMReviewSerializer(review)
            return Response(serializer.data)
        except LLMReview.DoesNotExist:
            return Response(
                {"detail": "LLM review not found for this proposal."},
                status=status.HTTP_404_NOT_FOUND
            )
