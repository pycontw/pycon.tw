from django.conf import settings
from django.template import Context, Library
from django.template.loader import get_template
from django.utils import translation

from events.models import KeynoteEvent, JobListingsEvent, Location
from sponsors.models import Sponsor, OpenRole
from proposals.utils import format_names

from datetime import datetime, timedelta
from math import floor

LOCATION_DISPLAY_DICT = {
    Location.R0: 'R0',
    Location.R1: 'R1',
    Location.R2: 'R2',
    Location.R3: 'R3',
    Location.R4: 'R4',
    Location.R012: 'R123',
}
ROW_UNIT = 5 * 60  # in seconds
MARKER_UNIT = 30 * 60  # in seconds

register = Library()


@register.simple_tag
def calc_grid_row(begin, end, timeline_start='08:30'):
    d_format = '%H:%M'
    start_point = datetime.strptime(timeline_start, d_format)

    def get_row(t):
        diff = datetime.strptime(t, d_format) - start_point
        return int(diff.seconds / ROW_UNIT)+1

    start_row = get_row(begin)
    end_row = get_row(end)
    return {'start_row': start_row, 'end_row': end_row}


@register.filter
def gen_timeline(start, end):
    timeline = [{'time': start, 'row_start': 1, 'row_end': 6}]
    d_format = '%H:%M'

    time_start = datetime.strptime(start, d_format)
    time_end = datetime.strptime(end, d_format)
    ticks_count = floor((time_end - time_start).seconds / MARKER_UNIT)

    scale_unit_multiplier = int(MARKER_UNIT / ROW_UNIT)  # 6 (magic number)
    time_next = time_start
    row_start_next = 1
    row_end_next = 6
    for i in range(ticks_count):
        time_next += timedelta(seconds=MARKER_UNIT)
        row_start_next += scale_unit_multiplier
        row_end_next += scale_unit_multiplier
        t = datetime.strftime(time_next, d_format)
        c = '--hour' if t.endswith('00') else '--half-an-hour'
        timeline.append({
            'time': t,
            'row_start': row_start_next,
            'row_end': row_end_next,
            'class': c
        })

    return timeline


@register.filter
def event_cell_class(event):
    event_class = {
        'events.customevent': 'custom',
        'events.keynoteevent': 'keynote',
        'events.proposedtalkevent': 'talk',
        'events.proposedtutorialevent': 'tutorial',
        'events.sponsoredevent': 'talk',
    }[event._meta.label_lower]
    classes = [event_class]
    if getattr(event, 'break_event', False):
        classes.append('is-break')
    return ' '.join(classes)


@register.filter
def event_tr_class(slot_info):
    for room, event in slot_info:
        if event._meta.label_lower == 'events.customevent':
            return 'custom'
    return ''


@register.filter
def room_display(value):
    return LOCATION_DISPLAY_DICT.get(value, '')


def get_custom_event_display(event):
    template = get_template('events/_includes/schedule_custom_event.html')
    return template.render({'event': event})


def get_keynote_event_display(event):
    template = get_template('events/_includes/schedule_keynote_event.html')
    return template.render({'event': event})


def _render_talk_event_template(event, info, speaker_names, sponsored):
    template = get_template('events/_includes/schedule_talk_event.html')
    return template.render({
        'event': event, 'info': info, 'sponsored': sponsored,
        'speakers': format_names(speaker_names),
    })


def get_talk_event_display(event):
    proposal = event.proposal
    speaker_names = [proposal.submitter.speaker_name]
    if getattr(event, '_additional_speaker_count', 1):
        speaker_names.extend(
            proposal.additionalspeaker_set
            .values_list('user__speaker_name', flat=True),
        )
    return _render_talk_event_template(event, proposal, speaker_names, False)


def get_tutorial_event_display(event):
    proposal = event.proposal
    speaker_names = [proposal.submitter.speaker_name]
    if getattr(event, '_additional_speaker_count', 1):
        speaker_names.extend(
            proposal.additionalspeaker_set
            .values_list('user__speaker_name', flat=True),
        )
    return _render_talk_event_template(event, proposal, speaker_names, False)


def get_sponsored_event_display(event):
    return _render_talk_event_template(
        event, event, [event.host.speaker_name], True,
    )


@register.filter
def event_display(event):
    with translation.override('en-us'):
        f = {
            'events.customevent': get_custom_event_display,
            'events.keynoteevent': get_keynote_event_display,
            'events.proposedtalkevent': get_talk_event_display,
            'events.proposedtutorialevent': get_tutorial_event_display,
            'events.sponsoredevent': get_sponsored_event_display,
        }[event._meta.label_lower]
        return f(event)


@register.filter
def event_date_display(event):
    try:
        date = event.begin_time.value.date()
    except AttributeError:
        return '‑'
    try:
        return settings.EVENTS_DAY_NAMES[date]
    except KeyError:
        return str(date)


@register.simple_tag
def get_keynote_events():
    return KeynoteEvent.objects.order_by('begin_time')


def _get_sponsors_with_open_roles():
    sponsor_has_open_role = set(OpenRole.objects.values_list('sponsor', flat=True))
    sponsor_set = Sponsor.objects.filter(id__in=sponsor_has_open_role).order_by('level')

    return sponsor_set


@register.simple_tag
def get_open_roles_of_sponsors():
    return _get_sponsors_with_open_roles()


@register.simple_tag
def get_open_roles():
    return OpenRole.objects.order_by('sponsor')
