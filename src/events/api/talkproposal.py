from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from events import models
from events import serializers

class TalkProposalViewSet(viewsets.ModelViewSet):
    queryset = models.TalkProposal.objects.all()
    serializer_class = serializers.TalkProposalListSerializer
