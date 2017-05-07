from django.template import Context, Library, Template
from django.utils import translation
from django.utils.html import format_html

from events.models import Location
from proposals.utils import format_names


LOCATION_DISPLAY_DICT = {
    Location.R0: 'R0',
    Location.R1: 'R1',
    Location.R2: 'R2',
    Location.R3: 'R3',
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
    return event.title


def get_keynote_event_display(event):
    return format_html(
        'Keynote: <span class="keynote-speaker">{name}</span>',
        name=event.speaker_name,
    )


TALK_EVENT_TEMPLATE = Template("""
<p class="talk-title">
  <a href="{{ event.get_absolute_url }}">{{ title }}</a>
</p>
<p class="talk-speakers">{{ speakers }}</p>
<p class="talk-tags">
  <span class="schedule-label lang-label"
      data-balloon="{{ language_display }}" data-balloon-pos="down">
    <span>{{ language_tag }}</span>
    <span class="schedule-label-description">{{ language_display }}</span>
  </span>
  <span class="schedule-label level-label"
      data-balloon="{{ level_display }}" data-balloon-pos="down">
    <span>{{ level_tag }}</span>
    <span class="schedule-label-description">{{ level_display }}</span>
  </span>
  {% if sponsored %}
  {% with label=_('Sponsored talk') %}
  <span class="schedule-label sponsor-label"
      data-balloon="{{ label }}" data-balloon-pos="down">
    <span class="fa fa-handshake-o"></span>
    <span class="schedule-label-description">{{ label }}</span>
  </span>
  {% endwith %}
  {% endif %}
  {% if not recording_policy %}
  <span class="schedule-label recording-label"
      data-balloon="No recording" data-balloon-pos="down">
    <span class="fa fa-microphone-slash"></span>
    <span class="schedule-label-description">No recording</span>
  </span>
  {% endif %}
</p>
""")


TALK_LANGUAGE_TAG_DICT = {
    'ENEN': 'E',
    'ZHEN': 'ZE',
    'ZHZH': 'Z',
    'TAI':  'T',
}

TALK_LEVEL_TAG_DICT = {
    'NOVICE': '–',
    'INTERMEDIATE': '=',
    'EXPERIENCED': '≡',
}


def _render_talk_event_template(event, info, speaker_names, sponsored):
    with translation.override('en-us'):
        return TALK_EVENT_TEMPLATE.render(Context({
            'event': event,
            'title': info.title,
            'language_display': info.get_language_display(),
            'language_tag': TALK_LANGUAGE_TAG_DICT[info.language],
            'level_display': info.get_python_level_display(),
            'level_tag': TALK_LEVEL_TAG_DICT[info.python_level],
            'speakers': format_names(speaker_names),
            'recording_policy': info.recording_policy,
            'sponsored': sponsored,
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
    f = {
        'events.customevent': get_custom_event_display,
        'events.keynoteevent': get_keynote_event_display,
        'events.proposedtalkevent': get_proposed_talk_event_display,
        'events.sponsoredevent': get_sponsored_event_display,
    }[event._meta.label_lower]
    return f(event)
