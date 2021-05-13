from rest_framework.generics import RetrieveAPIView
from rest_framework import views
from rest_framework.response import Response

from proposals.models import TutorialProposal
from events import models

from . import serializers

from django.conf import settings


class TalkDetailAPIView(RetrieveAPIView):

    queryset = models.TalkProposal.objects.all()
    serializer_class = serializers.TalkDetailSerializer


class TutorialListAPIView(views.APIView):
    def get(self, request):
        tutorial_data = TutorialProposal.objects.filter_accepted()

        response_data = {"tutorials": []}
        for tutorial in tutorial_data:
            response_data["tutorials"].append({
                "title": tutorial.title,
                "abstract": tutorial.abstract,
                "tutorial_id": tutorial.id
            })

         return Response(response_data)


class ScheduleAPIView(RetrieveAPIView):
    def get(self, request):
        queryset = models.Schedule.objects.all()

        response_data = {"schedule_html": [], "schedule_day": []}
        if queryset.exists():
            response_data["schedule_html"] = queryset.latest().html
        response_data["schedule_day"] = settings.EVENTS_DAY_NAMES.items()

        return Response(response_data)
