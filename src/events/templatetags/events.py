from django.conf import settings
from django.template import Context, Library
from django.template.loader import get_template
from django.utils import translation

from events.models import Location
from proposals.utils import format_names


LOCATION_DISPLAY_DICT = {
    Location.R0: 'R0',
    Location.R1: 'R1',
    Location.R2: 'R2',
    Location.R3: 'R3',
    Location.R4: 'R4',
    Location.R012: 'R123',
}

register = Library()


@register.filter
def event_cell_class(event):
    event_class = {
        'events.customevent': 'custom',
        'events.keynoteevent': 'keynote',
        'events.proposedtalkevent': 'talk',
        'events.sponsoredevent': 'talk',
    }[event._meta.label_lower]
    classes = [event_class]
    if getattr(event, 'break_event', False):
        classes.append('is-break')
    return ' '.join(classes)


@register.filter
def room_display(value):
    return LOCATION_DISPLAY_DICT.get(value, '')


def get_custom_event_display(event):
    template = get_template('events/_includes/schedule_custom_event.html')
    return template.render(Context({'event': event}))


def get_keynote_event_display(event):
    template = get_template('events/_includes/schedule_keynote_event.html')
    return template.render(Context({'event': event}))


def _render_talk_event_template(event, info, speaker_names, sponsored):
    template = get_template('events/_includes/schedule_talk_event.html')
    return template.render(Context({
        'event': event, 'info': info, 'sponsored': sponsored,
        'speakers': format_names(speaker_names),
    }))


def get_proposed_talk_event_display(event):
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
            'events.proposedtalkevent': get_proposed_talk_event_display,
            'events.sponsoredevent': get_sponsored_event_display,
        }[event._meta.label_lower]
        return f(event)


@register.filter
def event_date_display(event):
    return settings.EVENTS_DAY_NAMES[event.begin_time.value.date()]
