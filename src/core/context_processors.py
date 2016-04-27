from django.conf import settings


def google_analytics(request):
    return {'GA_TRACK_ID': settings.GA_TRACK_ID}


def proposals_states(requests):
    return {
        'proposals_creatable': settings.PROPOSALS_CREATABLE,
        'proposals_editable': settings.PROPOSALS_EDITABLE,
        'proposals_withdrawable': settings.PROPOSALS_WITHDRAWABLE,
    }
