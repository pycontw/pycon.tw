import collections
from typing import List, Union

from django.conf import settings
from django.db.models import Count
from django.http import Http404
from django.utils.timezone import make_naive
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentication import TokenAuthentication
from events.models import (
    CustomEvent,
    KeynoteEvent,
    Location,
    ProposedTalkEvent,
    ProposedTutorialEvent,
    SponsoredEvent,
    Time,
)

from . import serializers


class TalkListAPIView(ListAPIView):
    serializer_class = serializers.TalkListSerializer

    def get_queryset(self):
        queryset = ProposedTalkEvent.objects.all()
        category = self.kwargs.get('category')
        if category is not None:
            queryset = queryset.filter(proposal__category=category)
        return queryset


class SponsoredEventListAPIView(ListAPIView):
    serializer_class = serializers.SponsoredEventListSerializer

    def get_queryset(self):
        queryset = SponsoredEvent.objects.all()
        category = self.kwargs.get('category')
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset


class TutorialListAPIView(ListAPIView):
    serializer_class = serializers.TutorialListSerializer

    def get_queryset(self):
        queryset = ProposedTutorialEvent.objects.all()
        category = self.kwargs.get('category')
        if category is not None:
            queryset = queryset.filter(proposal__category=category)
        return queryset


class SpeechListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        event_type_string = request.GET.get("event_types")
        event_types = event_type_string.split(',') if event_type_string else []
        api_view_dict = {
            'talk': TalkListAPIView,
            'sponsored': SponsoredEventListAPIView,
            'tutorial': TutorialListAPIView,
        }

        data = []
        for event_type, api_view in api_view_dict.items():
            if event_types and event_type not in event_types:
                continue
            view = api_view.as_view()
            event_data = view(request._request, *args, **kwargs).data
            data.extend(event_data)

        if data:
            return Response(data)
        else:
            raise Http404


class SpeechListByCategoryAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = []
        for api_view in (SponsoredEventListAPIView, TalkListAPIView, TutorialListAPIView):
            view = api_view.as_view()
            event_data = view(request._request, *args, **kwargs).data
            data.extend(event_data)

        return Response(data)


class TalkDetailAPIView(RetrieveAPIView):
    queryset = ProposedTalkEvent.objects.all()
    serializer_class = serializers.TalkDetailSerializer


class SponsoredEventDetailAPIView(RetrieveAPIView):
    queryset = SponsoredEvent.objects.all()
    serializer_class = serializers.SponsoredEventDetailSerializer


class TutorialDetailAPIView(RetrieveAPIView):
    queryset = ProposedTutorialEvent.objects.all()
    serializer_class = serializers.TutorialDetailSerializer


class SpeechDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        event_id = self.kwargs.get('pk')
        event_type = self.kwargs.get('event_type')
        api_view_dict = {
            'talk': TalkDetailAPIView,
            'sponsored': SponsoredEventDetailAPIView,
            'tutorial': TutorialDetailAPIView,
        }

        if not event_id or not event_type or \
                event_type not in api_view_dict:
            raise Http404

        api_view = api_view_dict[event_type]
        view = api_view.as_view()
        return view(request._request, *args, **kwargs)


def _room_sort_key(room):
    return room.split('-', 1)[0]


class EventWrapper:

    def __init__(self, obj):
        self.obj = obj

    @property
    def event_id(self) -> int:
        return self.obj.id

    @property
    def event_type(self) -> str:
        type_map = {
            CustomEvent: 'custom',
            KeynoteEvent: 'keynote',
            ProposedTalkEvent: 'talk',
            SponsoredEvent: 'sponsored',
            ProposedTutorialEvent: 'tutorial',
        }
        return type_map[type(self.obj)]

    @property
    def title(self) -> Union[str, dict]:
        if isinstance(self.obj, KeynoteEvent):
            return {
                'zh_hant': self.obj.session_title_zh_hant,
                'en_us': self.obj.session_title_en_us,
            }
        elif isinstance(self.obj, (ProposedTalkEvent, ProposedTutorialEvent)):
            return self.obj.proposal.title
        else:
            return self.obj.title

    @property
    def speakers(self) -> Union[List[str], List[dict]]:
        if isinstance(self.obj, KeynoteEvent):
            return [
                {
                    'zh_hant': self.obj.speaker_name_zh_hant,
                    'en_us': self.obj.speaker_name_en_us,
                }
            ]
        if isinstance(self.obj, SponsoredEvent):
            return [self.obj.host.speaker_name]
        elif isinstance(self.obj, (ProposedTalkEvent, ProposedTutorialEvent)):
            speaker_names = [self.obj.proposal.submitter.speaker_name]
            if getattr(self.obj, '_additional_speaker_count', 1):
                speaker_names.extend(
                    self.obj.proposal.additionalspeaker_set
                    .values_list('user__speaker_name', flat=True),
                )
            return speaker_names
        else:
            return []

    @property
    def begin_time(self) -> str:
        return make_naive(self.obj.begin_time.value).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def end_time(self) -> str:
        return make_naive(self.obj.end_time.value).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def begin_time_utc(self) -> str:
        return self.obj.begin_time.value

    @property
    def end_time_utc(self) -> str:
        return self.obj.end_time.value

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
        elif isinstance(self.obj, SponsoredEvent):
            return self.obj.recording_policy
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
        elif isinstance(self.obj, SponsoredEvent):
            return self.obj.language
        else:
            return ''

    @property
    def python_level(self) -> str:
        if isinstance(self.obj, (ProposedTalkEvent, ProposedTutorialEvent)):
            return self.obj.proposal.python_level
        elif isinstance(self.obj, SponsoredEvent):
            return self.obj.python_level
        else:
            return ''

    def display(self):
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'title': self.title,
            'speakers': self.speakers,
            'begin_time': self.begin_time_utc,
            'end_time': self.end_time_utc,
            'is_remote': self.is_remote,
            'recording_policy': self.recording_policy,
            'language': self.language,
            'python_level': self.python_level,
            'break_event': self.break_event,
        }


class ScheduleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    event_querysets = [
        CustomEvent.objects.all().exclude(location=Location.OTHER),
        KeynoteEvent.objects.all().exclude(location=Location.OTHER),
        (
            ProposedTalkEvent.objects
            .select_related('proposal__submitter')
            .annotate(_additional_speaker_count=Count(
                'proposal__additionalspeaker_set',
            )).exclude(location=Location.OTHER)
        ),
        SponsoredEvent.objects.select_related('host').exclude(location=Location.OTHER),
        (
            ProposedTutorialEvent.objects
            .select_related('proposal__submitter')
            .annotate(_additional_speaker_count=Count(
                'proposal__additionalspeaker_set',
            )).exclude(location=Location.OTHER)
        ),
    ]

    def get(self, request):
        begin_time_event_dict = collections.defaultdict(set)
        for qs in self.event_querysets:
            for event in qs.select_related('begin_time', 'end_time'):
                begin_time_event_dict[event.begin_time].add(event)

        day_info_dict = collections.OrderedDict(
            (str(date), {
                'date': date,
                'name': name,
                'rooms': set(),
                'slots': {},
                'timeline': {},
            }) for date, name in settings.EVENTS_DAY_NAMES.items()
        )

        times = list(Time.objects.order_by('value'))

        for begin in times:
            try:
                day_info = day_info_dict[str(begin.value.date())]
            except KeyError:
                continue

            for event in begin_time_event_dict[begin]:
                location = event.location
                day_info['slots'].setdefault(location, [])
                day_info['timeline'].setdefault('begin', event.begin_time)
                day_info['timeline'].setdefault('end', event.end_time)

                event_obj = EventWrapper(event)

                day_info['slots'][location].append(event_obj.display())
                day_info['timeline']['begin'] = min(
                    day_info['timeline']['begin'],
                    event.begin_time
                )
                day_info['timeline']['end'] = max(
                    day_info['timeline']['end'],
                    event.end_time
                )

                day_info['rooms'].add(location)

        for info in day_info_dict.values():
            # Sort rooms.
            info['rooms'] = sorted(info['rooms'], key=_room_sort_key)

        result = []
        for day_info in day_info_dict.values():
            day_info['timeline']['begin'] = day_info['timeline']['begin'].value
            day_info['timeline']['end'] = day_info['timeline']['end'].value
            result.append(day_info)

        return Response({'data': result})


class KeynoteEventListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = KeynoteEvent.objects.all()
    serializer_class = serializers.KeynoteEventSerializer
