from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from core.authentication import TokenAuthentication
from events.models import ProposedTutorialEvent, SponsoredEvent, Schedule, KeynoteEvent
from proposals.models import TalkProposal, TutorialProposal

from . import serializers


class TalkDetailAPIView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TalkProposal.objects.all()
    serializer_class = serializers.TalkDetailSerializer


class TalkListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = TalkProposal.objects.filter_accepted()
    serializer_class = serializers.TalkListSerializer


class SponsoredEventListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = SponsoredEvent.objects.all()
    serializer_class = serializers.SponsoredEventSerializer


class TutorialDetailAPIView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ProposedTutorialEvent.objects.all()
    serializer_class = serializers.TutorialDetailSerializer


class TutorialListAPIView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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



class EventWrapper:

    def __init__(self, obj):
        self.obj = obj

    @property
    def event_id(self) -> int:
        return self.obj.id

    @property
    def event_type(self) -> str:
        TYPE_MAP = {
            CustomEvent: 'custom',
            KeynoteEvent: 'keynote',
            ProposedTalkEvent: 'talk',
            SponsoredEvent: 'sponsored',
            ProposedTutorialEvent: 'tutorial',
        }
        return TYPE_MAP[type(self.obj)]

    @property
    def title(self) -> str:
        if isinstance(self.obj, KeynoteEvent):
            return self.obj.session_title
        elif isinstance(self.obj, (ProposedTalkEvent, ProposedTutorialEvent)):
            return self.obj.proposal.title
        else:
            return self.obj.title

    @property
    def speakers(self) -> str:
        if isinstance(self.obj, KeynoteEvent):
            return self.obj.speaker_name
        elif isinstance(self.obj, (ProposedTalkEvent, ProposedTutorialEvent)):
            speaker_names = [self.obj.proposal.submitter.speaker_name]
            if getattr(self.obj, '_additional_speaker_count', 1):
                speaker_names.extend(
                    self.obj.proposal.additionalspeaker_set
                    .values_list('user__speaker_name', flat=True),
                )
            return ', '.join(speaker_names)
        else:
            return ''

    @property
    def begin_time(self) -> str:
        return self.obj.begin_time.value.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def end_time(self) -> str:
        return self.obj.end_time.value.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def is_remote(self) -> bool:
        if isinstance(self.obj, (KeynoteEvent, ProposedTalkEvent, ProposedTutorialEvent)):
            return self.obj.is_remote
        else:
            return False

    @property
    def recording_policy(self) -> bool:
        if isinstance(self.obj, (KeynoteEvent, CustomEvent)):
            return True
        else:
            return self.obj.proposal.recording_policy

    @property
    def break_event(self) -> bool:
        if isinstance(self.obj, CustomEvent):
            return self.obj.break_event
        else:
            return False

    @property
    def language(self) -> str:
        if isinstance(self.obj, (ProposedTalkEvent, ProposedTutorialEvent)):
            return self.obj.proposal.language
        else:
            return ''

    @property
    def python_level(self) -> str:
        if isinstance(self.obj, (ProposedTalkEvent, ProposedTutorialEvent)):
            return self.obj.proposal.python_level
        else:
            return ''

    def display(self):
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'title': self.title,
            'speakers': self.speakers,
            'begin_time': self.begin_time,
            'end_time': self.end_time,
            'is_remote': self.is_remote,
            'recording_policy': self.recording_policy,
            'language': self.language,
            'python_level': self.python_level,
            'break_event': self.break_event,
        }



    def get(self, request):
        queryset = Schedule.objects.all()

        response_data = {"schedule_html": [], "schedule_day": []}
        if queryset.exists():
            response_data["schedule_html"] = queryset.latest().html
        response_data["schedule_day"] = settings.EVENTS_DAY_NAMES.items()

        return Response(response_data)


class KeynoteEventListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = KeynoteEvent.objects.all()
    serializer_class = serializers.KeynoteEventSerializer
