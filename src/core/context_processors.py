from django.conf import settings

from core.utils import OrderedDefaultDict
from sponsors.models import Sponsor


def pycontw(request):
    return {
        'GA_TRACK_ID': settings.GA_TRACK_ID,
        'KKTIX_URL': 'https://pycontw.kktix.cc/events/pycontw2017',
        'VOLUNTEER_FORM_URL': (
            'https://docs.google.com/forms/d/e/'
            '1FAIpQLSfnTEpD_I74Yeji6GqfI-YSZoYgg7Ax-YCEG5PNHrBusTgn4Q/viewform'
        ),
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


def sponsors(request):
    groups = OrderedDefaultDict(list)
    for sponsor in Sponsor.objects.order_by('level'):
        groups[sponsor.level].append(sponsor)
    return {
        'sponsor_groups': groups,
    }
