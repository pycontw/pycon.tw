import collections
import functools
import urllib.parse

from django.core.serializers.json import DjangoJSONEncoder


SITE_PREFIX = 'https://tw.pycon.org/2016/media/'

USER_DUMP_KEYS = [
    'bio', 'email', 'speaker_name',
    'facebook_profile_url', 'github_id', 'twitter_id',
]

PROPOSAL_DUMP_KEYS = SPONSORED_EVENT_DUMP_KEYS = [
    'abstract', 'category', 'detailed_description', 'language', 'python_level',
    'recording_policy', 'slide_link', 'title',
]


def dump_user(user):
    data = {key: getattr(user, key) for key in USER_DUMP_KEYS}
    if user.photo:
        data['photo_url'] = urllib.parse.urljoin(SITE_PREFIX, user.photo.url)
    return data


def dump_proposal(proposal):
    data = {key: getattr(proposal, key) for key in PROPOSAL_DUMP_KEYS}
    data['speakers'] = [dump_user(info.user) for info in proposal.speakers]
    return data


def dump_sponsored_event_detail(event):
    data = {key: getattr(event, key) for key in SPONSORED_EVENT_DUMP_KEYS}
    data['speakers'] = [dump_user(event.host)]
    return data


json_encoder = DjangoJSONEncoder()


def event_dumper(f):
    """Decorator to provide dumping of common event fields.
    """
    @functools.wraps(f)
    def inner(obj):
        data = {
            'begin_time': json_encoder.encode(obj.begin_time.value).strip('"'),
            'end_time': json_encoder.encode(obj.end_time.value).strip('"'),
            'location': obj.location,
        }
        data.update(f(obj))
        return data

    return inner


@event_dumper
def dump_keynote_event(event):
    return {
        'type': 'keynote',
        'speakers': [event.speaker_name],
    }


@event_dumper
def dump_custom_event(event):
    return {
        'type': 'custom',
        'title': event.title,
    }


@event_dumper
def dump_sponsored_event(event):
    return {
        'type': 'sponsored_talk',
        'title': event.title,
        'speakers': [event.host.speaker_name],
        'detail_id': 'sponsored_{}'.format(event.pk)
    }


@event_dumper
def dump_proposed_talk_event(event):
    return {
        'type': 'talk',
        'title': event.proposal.title,
        'speakers': [
            speaker.user.speaker_name
            for speaker in event.proposal.speakers
        ],
        'detail_id': str(event.proposal.pk),
    }


EVENT_LOADERS = {
    'keynoteevent': dump_keynote_event,
    'customevent': dump_custom_event,
    'sponsoredevent': dump_sponsored_event,
    'proposedtalkevent': dump_proposed_talk_event,
}


def dump_schedule(event_iter):
    schedule_data_lists = collections.defaultdict(list)
    for event in event_iter:
        loader = EVENT_LOADERS[event._meta.model_name]
        data = loader(event)
        key = data['begin_time'].split('T', 1)[0]
        schedule_data_lists[key].append(data)
    for data_list in schedule_data_lists.values():
        data_list.sort(key=lambda data: (data['begin_time'], data['location']))
    return schedule_data_lists
