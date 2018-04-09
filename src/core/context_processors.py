import itertools
import operator

from django.conf import settings
from django.utils.translation import get_language

from sponsors.models import Sponsor


def _build_google_form_url(uid):
    return 'https://docs.google.com/forms/d/e/{uid}/viewform'.format(uid=uid)


def pycontw(request):
    lang = get_language()
    if lang and lang.startswith('zh'):
        sponsor_id = '1FAIpQLSf5pgDeYtspU1AfexFlAw-gZXWjcXhPxNTj7HGb258bD-0Eig'
        volun_id = '1FAIpQLSe7-q3Ae3yBA4TepszIMCCHQzU3hg8Hy03X-9VcCv7DO5f_oA'
    else:
        sponsor_id = '1FAIpQLSeB7I99Jugc9qGqzxZfF_sYQTz3nE7--NDu0hHhoBpYSqrtyg'
        volun_id = '1FAIpQLSeEHdCEv7R_BQb6eawQpndSlEPLpUHQDoc7URvJU0fpFeJHIA'
    return {
        'GTM_TRACK_ID': settings.GTM_TRACK_ID,
        'KKTIX_URL': 'https://pycontw.kktix.cc/events/pycontw2017',
        'SPONSOR_FORM_URL': _build_google_form_url(sponsor_id),
        'VOLUNTEER_FORM_URL': _build_google_form_url(volun_id),
    }


def proposals_states(request):
    return {
        'proposals_creatable': settings.PROPOSALS_CREATABLE,
        'proposals_editable': settings.PROPOSALS_EDITABLE,
        'proposals_withdrawable': settings.PROPOSALS_WITHDRAWABLE,
    }


def reviews_states(request):
    return {
        'reviews_stage': settings.REVIEWS_STAGE,
        'reviews_public': settings.REVIEWS_VISIBLE_TO_SUBMITTERS,
    }


def iter_sponsor_section():
    groups = itertools.groupby(
        Sponsor.objects.order_by('level'),
        key=operator.methodcaller('get_level_display'),
    )
    for k, v in groups:
        yield k, list(v)


def sponsors(request):
    return {
        'sponsors': Sponsor.objects.order_by('level'),
        'sponsor_sections': iter_sponsor_section(),
    }
