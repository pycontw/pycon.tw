import os

from django.utils.translation import gettext_lazy as _
from .base import BASE_DIR, STATICFILES_DIRS, TEMPLATES
from .base import *     # noqa

# Override static and media URL for prefix in WSGI server.
# https://code.djangoproject.com/ticket/25598
STATIC_URL = '/prs/static/'
MEDIA_URL = '/prs/media/'

CONFERENCE_DEFAULT_SLUG = 'pycontw-2021'

TALK_PROPOSAL_DURATION_CHOICES = (
    ('NOPREF', _('No preference')),
    ('PREF15', _('Prefer 15min')),
    ('PREF30', _('Prefer 30min')),
    ('PREF45', _('Prefer 45min')),
)

TEMPLATES[0]['DIRS'][1] = os.path.join(
    BASE_DIR, 'templates', CONFERENCE_DEFAULT_SLUG,
)
STATICFILES_DIRS[1] = os.path.join(
    BASE_DIR, 'static', CONFERENCE_DEFAULT_SLUG, '_includes',
)

FRONTEND_HOST = 'https://tw.pycon.org/2021'
