from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import views
from rest_framework.response import Response

from django.conf import settings

from events.models import ProposedTutorialEvent, SponsoredEvent, Schedule, KeynoteEvent
from proposals.models import TalkProposal, TutorialProposal

from . import serializers


class TalkDetailAPIView(RetrieveAPIView):

    queryset = TalkProposal.objects.all()
    serializer_class = serializers.TalkDetailSerializer


class TalkListAPIView(ListAPIView):

    queryset = TalkProposal.objects.filter_accepted()
    serializer_class = serializers.TalkListSerializer


class SponsoredEventListAPIView(ListAPIView):

    queryset = SponsoredEvent.objects.all()
    serializer_class = serializers.SponsoredEventSerializer


class TutorialDetailAPIView(RetrieveAPIView):

    queryset = ProposedTutorialEvent.objects.all()
    serializer_class = serializers.TutorialDetailSerializer


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
        queryset = Schedule.objects.all()

        response_data = {"schedule_html": [], "schedule_day": []}
        if queryset.exists():
            response_data["schedule_html"] = queryset.latest().html
        response_data["schedule_day"] = settings.EVENTS_DAY_NAMES.items()

        return Response(response_data)


class KeynoteEventListAPIView(views.APIView):
    def get(self, request):
        queryset = KeynoteEvent.objects.all()
        serializer_class = serializers.KeynoteEventSerializer(queryset, many=True)
        return Response(serializer_class.data)
