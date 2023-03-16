from django.conf import settings
from django.template import Library

from events.models import KeynoteEvent
from sponsors.models import OpenRole, Sponsor

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
