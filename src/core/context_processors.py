import itertools
import operator

from django.conf import settings
from django.urls import get_script_prefix
from django.utils.translation import get_language

from sponsors.models import Sponsor, OpenRole


def _build_google_form_url(uid):
    return 'https://docs.google.com/forms/d/e/{uid}/viewform'.format(uid=uid)


def script_prefix(request):
    return {
        'SCRIPT_PREFIX': get_script_prefix(),
    }


def pycontw(request):
    lang = get_language()
    if lang and lang.startswith('zh'):
        sponsor_id = '1FAIpQLScEIeCrTHNvwbdNbZt4nK1mteC6NzHtXgF5bVn1KTtR0_sorA'
        volun_id = '1FAIpQLSfdqEqqjzPnVU7S8ya1slXKszSIHOpljKEzY8odGRBjjAv-fw'
    else:
        sponsor_id = '1FAIpQLScEIeCrTHNvwbdNbZt4nK1mteC6NzHtXgF5bVn1KTtR0_sorA'
        volun_id = '1FAIpQLSfdqEqqjzPnVU7S8ya1slXKszSIHOpljKEzY8odGRBjjAv-fw'
    return {
        'GTM_TRACK_ID': settings.GTM_TRACK_ID,
        'KKTIX_URL': {
            'RSVD': 'https://pycontw.kktix.cc/events/20200905-reserved',
            'INDI': 'https://pycontw.kktix.cc/events/20200905-individual',
            'CORP': 'https://pycontw.kktix.cc/events/20200905-corporate',
        },
        'SPONSOR_FORM_URL': _build_google_form_url(sponsor_id),
        'VOLUNTEER_FORM_URL': _build_google_form_url(volun_id),
    }


def _iter_sponsor_section():
    groups = itertools.groupby(
        Sponsor.objects.order_by('level'),
        key=operator.methodcaller('get_level_display'),
    )
    for k, v in groups:
        yield k, list(v)


def sponsors(request):
    return {
        'sponsors': Sponsor.objects.order_by('level'),
        'sponsor_sections': _iter_sponsor_section(),
    }


def _get_sponsors_with_open_roles():
    sponsor_set = set()
    for sponsor in Sponsor.objects.order_by('level'):
        for open_role in OpenRole.objects.order_by('sponsor'):
            if open_role.sponsor.name == sponsor.name:
                sponsor_set.add(sponsor)

    return sponsor_set


def open_roles_of_sponsors(request):
    return {
        'open_role_sponsors': _get_sponsors_with_open_roles(),
        'open_roles': OpenRole.objects.order_by('sponsor'),
    }


def events(request):
    return {'schedule_redirect_url': settings.SCHEDULE_REDIRECT_URL}
