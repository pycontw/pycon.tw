import operator

from django.conf import settings
from django.http import JsonResponse
from django.templatetags.static import static
from django.utils import translation
from django.utils.encoding import force_str
from django.utils.translation import pgettext_lazy
from django.views.generic import View, TemplateView

from core.utils import TemplateExistanceStatusResponse
from core.views import IndexView
from events.models import (
    CustomEvent, KeynoteEvent,
    ProposedTalkEvent, ProposedTutorialEvent,
    SponsoredEvent,
)
from proposals.models import PrimarySpeaker


def _get_lazy_display(instance, attr):
    """Django's ``get_XXX_display()`` resolve lazy strings, we don't want that.

    This duplicates the actual implementation (except calling ``force_str()``)
    so we can get the underlying lazy object for translation later.

    github.com/django/django/blob/8dd5877f58f84f2/django/db/models/base.py#L929
    """
    field = instance._meta.get_field(attr)
    value = getattr(instance, attr)
    return dict(field.flatchoices).get(value, value)


def _iter_translations(value):
    for code, locale in [('zh', 'zh-hant'), ('en', 'en-us')]:
        with translation.override(locale):
            if isinstance(value, dict):
                tran = value[code]
            else:
                tran = force_str(value)
        yield code, tran


def _transform_translatable(key, value):
    data = {'id': key}
    for code, value in _iter_translations(value):
        data[code] = {'name': value}
    return data


def _transform_event_speaker(request, user):
    data = {
        'id': f'speaker-{user.pk}',
        'avatar': request.build_absolute_uri(user.get_thumbnail_url()),
        'zh': {},
        'en': {},
    }
    for key, value in [('name', user.get_full_name()), ('bio', user.bio)]:
        for code, tran in _iter_translations(value):
            data[code][key] = tran
    return data


class _FakeEventInfo:

    def __init__(self, pk, title, abstract, slide_link, speakers):
        self.title = title
        self.pk = pk
        self.abstract = abstract
        self.slide_link = slide_link
        self._speakers = speakers

    def __bool__(self):
        return False

    @property
    def speakers(self):
        for s in self._speakers:
            yield s


def _get_empty_event_info(event):
    return _FakeEventInfo(
        pk=event.pk, title=str(event),
        abstract=None, slide_link=None,
        speakers=[],
    )


class _KeynoteUser:

    def __init__(self, pk, speaker_name, bio, photo):
        self.pk = pk
        self.speaker_name = speaker_name
        self.bio = bio
        self.photo = photo

    def get_full_name(self):
        return self.speaker_name

    def get_thumbnail_url(self):
        return static(self.photo)


def _get_keynote_event_info(event):
    data = event.get_static_data()

    user = _KeynoteUser(
        pk=event.slug,
        speaker_name={k: v['name'] for k, v in data['speaker'].items()},
        bio={k: v['bio'] for k, v in data['speaker'].items()},
        photo=data['photo'],
    )
    event_info = _FakeEventInfo(
        pk=event.slug,
        title={k: v['title'] for k, v in data['session'].items()},
        abstract={k: v['description'] for k, v in data['session'].items()},
        slide_link=None,
        speakers=[PrimarySpeaker(user=user)],
    )

    return event_info


def _transform_session(request, event, type_key, info_getter):
    event_info = info_getter(event)

    if isinstance(event_info, _FakeEventInfo):
        tags = []
    else:
        tags = [
            _transform_translatable(
                f'lng-{event_info.language}',
                _get_lazy_display(event_info, 'language'),
            ),
            _transform_translatable(
                f'cat-{event_info.category}',
                _get_lazy_display(event_info, 'category'),
            ),
            _transform_translatable(
                f'lvl-{event_info.python_level}',
                _get_lazy_display(event_info, 'python_level'),
            ),
        ]

    room = None
    try:
        from ext2020.models import CommunityTrackEvent
        if isinstance(event, CommunityTrackEvent):
            room = _transform_translatable(
                str(event.venue),
                _get_lazy_display(event, 'venue'),
            )
    except ImportError:
        # Do not need to display for community track
        pass

    if not room:
        room = _transform_translatable(
            event.location,
            _get_lazy_display(event, 'location'),
        )

    speakers = [
        _transform_event_speaker(request, speaker.user)
        for speaker in event_info.speakers
    ]

    session = {
        'id': f'{type_key}-{event_info.pk}',
        'type': type_key,

        'start': event.begin_time.value.isoformat(),
        'end': event.end_time.value.isoformat(),
        'slide': event_info.slide_link,
        'speakers': [speaker['id'] for speaker in speakers],
        'tags': [tag['id'] for tag in tags],
        'en': {},
        'zh': {},

        # Our data structure does not distinguish between broadcast and live
        # presentation, so let's just treat broadcasted events as a special
        # kind of room.
        'room': room['id'],
        'broadcast': [],

        # TODO: What are these?
        'qa': None,
        'live': None,
        'record': None,
    }
    for key, value in [
            ('title', event_info.title),
            ('description', event_info.abstract)]:
        for code, tran in _iter_translations(value):
            session[code][key] = tran

    return session, speakers, tags, room


class CCIPAPIView(View):
    def get(self, request):
        session_sources = [
            (
                'event',
                pgettext_lazy('CCIP event type', 'event'),
                CustomEvent.objects.filter(break_event=False).select_related(
                    'begin_time', 'end_time',
                ),
                _get_empty_event_info,
            ),
            (
                'break',
                pgettext_lazy('CCIP event type', 'break'),
                CustomEvent.objects.filter(break_event=True).select_related(
                    'begin_time', 'end_time',
                ),
                _get_empty_event_info,
            ),
            (
                'keynote',
                pgettext_lazy('CCIP event type', 'keynote'),
                KeynoteEvent.objects.select_related('begin_time', 'end_time'),
                _get_keynote_event_info,
            ),
            (
                'sponsored',
                pgettext_lazy('CCIP event type', 'sponsored'),
                SponsoredEvent.objects.select_related(
                    'begin_time', 'end_time', 'host',
                ),
                lambda event: event,
            ),
            (
                'tutorial',
                pgettext_lazy('CCIP event type', 'tutorial'),
                (
                    ProposedTutorialEvent.objects
                    .select_related(
                        'begin_time', 'end_time',
                        'proposal', 'proposal__submitter',
                    )
                ),
                operator.attrgetter('proposal'),
            ),
            (
                'talk',
                pgettext_lazy('CCIP event type', 'talk'),
                (
                    ProposedTalkEvent.objects.select_related(
                        'begin_time', 'end_time', 'proposal', 'proposal__submitter',)
                ),
                operator.attrgetter('proposal'),
            ),
        ]

        try:
            from ext2020.models import CommunityTrackEvent
            session_sources.append((
                'community-track',
                pgettext_lazy('CCIP event type', 'community track'),
                CommunityTrackEvent.objects.filter(
                    order__in=[1, 2, 3, 4],
                    sponsored_event__isnull=True)
                .select_related(
                    'begin_time', 'end_time', 'venue',
                    'talk', 'talk__submitter'
                ).all(),
                operator.attrgetter('talk'),
            ),)
        except ImportError:
            # Do not need to display for community track
            pass

        rooms = {}
        session_types = []
        sessions = []
        speakers = {}
        tags = {}
        for type_key, type_name, queryset, info_getter in session_sources:
            session_types.append(_transform_translatable(type_key, type_name))
            for event in queryset.all():
                session, sess_speakers, sess_tags, room = _transform_session(
                    request=request, event=event,
                    type_key=type_key, info_getter=info_getter,
                )
                rooms[room['id']] = room
                speakers.update({s['id']: s for s in sess_speakers})
                tags.update({t['id']: t for t in sess_tags})
                sessions.append(session)

        def _room_sort_key(v):
            return v['id'].split('-', 1)[-1]

        return JsonResponse({
            'rooms': sorted(rooms.values(), key=_room_sort_key),
            'sessions': sessions,
            'session_types': session_types,
            'speakers': list(speakers.values()),
            'tags': list(tags.values()),
        }, safe=False)


class CCIPSponsorsView(IndexView):
    template_name = 'ccip/sponsors.html'
    response_class = TemplateExistanceStatusResponse


class CCIPStaffView(TemplateView):
    template_name = 'ccip/staff.html'
    response_class = TemplateExistanceStatusResponse
