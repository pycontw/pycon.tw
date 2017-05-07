from django.template import Context, Library, Template

from events.models import BaseEvent
from proposals.utils import format_names


LOCATION_DICT = dict(BaseEvent.LOCATION_CHOICES)

register = Library()


@register.filter
def event_cell_class(event):
    return {
        'events.customevent': 'custom',
        'events.proposedtalkevent': 'talk',
    }[event._meta.label_lower]


@register.filter
def room_display(value):
    return LOCATION_DICT[value]


def get_custom_event_display(event):
    return event.title


TALK_EVENT_TEMPLATE = Template("""
{% load i18n %}
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
    <span class="schedule-label-description">{% trans 'No recording' %}</span>
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


def get_proposed_talk_event_display(event):
    proposal = event.proposal
    speaker_names = [proposal.submitter.speaker_name]
    if getattr(event, '_additional_speaker_count', 1):
        speaker_names.extend(
            proposal.additionalspeaker_set
            .values_list('user__speaker_name', flat=True),
        )
    return TALK_EVENT_TEMPLATE.render(Context({
        'event': event,
        'title': proposal.title,
        'language_display': proposal.get_language_display(),
        'speakers': format_names(speaker_names),
        'language_tag': TALK_LANGUAGE_TAG_DICT[proposal.language],
        'sponsored': False,
    }))


@register.filter
def event_display(event):
    f = {
        'events.customevent': get_custom_event_display,
        'events.proposedtalkevent': get_proposed_talk_event_display,
    }[event._meta.label_lower]
    return f(event)
