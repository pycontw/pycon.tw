import collections

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from events import models
from . import serializers

from django.conf import settings


class TalkDetailAPIView(RetrieveAPIView):

    queryset = models.TalkProposal.objects.all()
    serializer_class = serializers.TalkDetailSerializer


class ScheduleAPIView(RetrieveAPIView):
    
    def get(self, request):
        queryset = models.Schedule.objects.all()

        response_data = {"schedule_html": [], "schedule_day": []}
        if (len(queryset) > 0):
            response_data["schedule_html"] = queryset[0].html
        response_data["schedule_day"] = settings.EVENTS_DAY_NAMES.items()

        return Response(response_data)

