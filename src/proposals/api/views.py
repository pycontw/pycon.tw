from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.authentication import TokenAuthentication
from proposals.models import TalkProposal, TutorialProposal
from reviews.models import Review


class ProposalSummaryAPIView(views.APIView):

    authentication_classes = [TokenAuthentication]
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
