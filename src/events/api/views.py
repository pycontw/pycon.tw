from rest_framework.generics import RetrieveAPIView
from rest_framework import views
from rest_framework.response import Response
from proposals.models import TutorialProposal
from events import models
from . import serializers


class TalkDetailAPIView(RetrieveAPIView):

    queryset = models.TalkProposal.objects.all()
    serializer_class = serializers.TalkDetailSerializer


class TutorialListAPIView(views.APIView):
    def get(self, request):
        tutorial_data = TutorialProposal.objects.all()

        response_data = {"tutorials": []}
        for tutorial in tutorial_data:
            response_data["tutorials"].append({
                "title": tutorial.title,
                "abstract": tutorial.abstract,
                "tutorial_id": tutorial.id
            })

        return Response(response_data)
