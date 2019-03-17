import itertools
import operator

from django.conf import settings
from django.core.urlresolvers import get_script_prefix
from django.utils.translation import get_language

from sponsors.models import Sponsor


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
        volun_id = '1FAIpQLSeEs59DrqXo3dYS9Cg52sa2MtPurTwpb0XD_s6U7W4HEqYifA'
    else:
        sponsor_id = '1FAIpQLScEIeCrTHNvwbdNbZt4nK1mteC6NzHtXgF5bVn1KTtR0_sorA'
        volun_id = '1FAIpQLScslZSIKPylGvnw2yFNMEINIdoA1avj89FrIfOP2N9H0xbCrg'
    return {
        'GTM_TRACK_ID': settings.GTM_TRACK_ID,
        'KKTIX_URL': {
            'RSVD': 'https://pycontw.kktix.cc/events/20180601-reserved',
            'INDI': 'https://pycontw.kktix.cc/events/20180601-individual',
            'CORP': 'https://pycontw.kktix.cc/events/20180601-corporate',
        },
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
