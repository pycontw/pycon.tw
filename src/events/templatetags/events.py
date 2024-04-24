from django.conf import settings
from django.template import Library

from events.models import KeynoteEvent

register = Library()


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
