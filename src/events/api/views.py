from rest_framework import views
from rest_framework.generics import RetrieveAPIView, ListAPIView

from events import models
from proposals.models import TalkProposal

from . import serializers


class TalkDetailAPIView(RetrieveAPIView):

    queryset = TalkProposal.objects.all()
    serializer_class = serializers.TalkDetailSerializer


class TalkListAPIView(ListAPIView):

    queryset = TalkProposal.objects.filter_accepted()
    serializer_class = serializers.TalkListSerializer
