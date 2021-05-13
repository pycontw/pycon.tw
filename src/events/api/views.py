from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from django.conf import settings

from events.models import SponsoredEvent, Schedule
from proposals.models import TalkProposal

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


class ScheduleAPIView(RetrieveAPIView):
    def get(self, request):
        queryset = Schedule.objects.all()

        response_data = {"schedule_html": [], "schedule_day": []}
        if queryset.exists():
            response_data["schedule_html"] = queryset.latest().html
        response_data["schedule_day"] = settings.EVENTS_DAY_NAMES.items()

        return Response(response_data)
