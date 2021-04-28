from datetime import datetime
from collections import namedtuple

from django.conf import settings
from django.utils import timezone

from registry.helper import reg


# This code is located here, but not in context_processor
# because this is not intended to be processed at every page
# preparing these requires database query, and only a subset of
# pages in dashboard need them

ProposalsState = namedtuple('ProposalsState', ['proposals_creatable',
                                               'proposals_editable',
                                               'proposals_withdrawable'])


def proposals_state():
    slug = settings.CONFERENCE_DEFAULT_SLUG

    state = ProposalsState(
        proposals_creatable=reg.get(f'{slug}.proposals.creatable', False),
        proposals_editable=reg.get(f'{slug}.proposals.editable', False),
        proposals_withdrawable=reg.get(f'{slug}.proposals.withdrawable', False),
    )

    # proposals.disable.after has a high priority if it is set
    disable_after = None

    try:
        disable_after_raw = reg.get(f'{slug}.proposals.disable.after', None)
        disable_after = datetime.strptime(disable_after_raw, '%Y-%m-%d %H:%M:%S%z')

        if timezone.now() >= disable_after:
            state = ProposalsState(
                proposals_creatable=False,
                proposals_editable=False,
                proposals_withdrawable=False,
            )

    except (ValueError, TypeError):
        pass

    return state


ReviewsState = namedtuple('ReviewsState', ['reviews_stage',
                                           'reviews_public',
                                           'reviews_enough'])


def reviews_state():
    slug = settings.CONFERENCE_DEFAULT_SLUG

    # return {
    #     'reviews_stage': reg.get(f'{slug}.reviews.stage', 0),
    #     'reviews_public': reg.get(f'{slug}.reviews.visible.to.submitters', False),
    # }

    return ReviewsState(
        reviews_stage=reg.get(f'{slug}.reviews.stage', 0),
        reviews_public=reg.get(f'{slug}.reviews.visible.to.submitters', False),
        reviews_enough=reg.get(f'{slug}.reviews.enough', 10),
    )
