import os

from django.utils.translation import gettext_lazy as _
from .base import BASE_DIR, STATICFILES_DIRS, TEMPLATES
from .base import *     # noqa

DEBUG=True

CONFERENCE_DEFAULT_SLUG = 'pycontw-2021'

TALK_PROPOSAL_DURATION_CHOICES = (
    ('NOPREF', _('No preference')),
    ('PREF15', _('Prefer 15min')),
    ('PREF30', _('Prefer 30min')),
    ('PREF45', _('Prefer 45min')),
)

TEMPLATES[0]['DIRS'][1] = os.path.join(BASE_DIR, 'templates', 'pycontw-2021')
STATICFILES_DIRS[1] = os.path.join(
    BASE_DIR, 'static', CONFERENCE_DEFAULT_SLUG, '_includes',
)

EVENTS_PUBLISHED = False
