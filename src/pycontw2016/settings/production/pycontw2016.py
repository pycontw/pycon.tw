from django.utils.translation import ugettext_lazy as _

from .base import *     # noqa

# Override static and media URL for prefix in WSGI server.
# https://code.djangoproject.com/ticket/25598
STATIC_URL = '/2016/static/'
MEDIA_URL = '/2016/media/'

CONFERENCE_DEFAULT_SLUG = 'pycontw-2016'

TALK_PROPOSAL_DURATION_CHOICES = (
    ('NOPREF', _('No preference')),
    ('PREF25', _('Prefer 25min')),
    ('PREF45', _('Prefer 45min')),
)
