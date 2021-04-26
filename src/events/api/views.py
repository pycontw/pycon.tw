from rest_framework.generics import RetrieveAPIView

from events import models
from . import serializers


class TalkDetailAPIView(RetrieveAPIView):

    queryset = models.TalkProposal.objects.all()
    serializer_class = serializers.TalkDetailSerializer
