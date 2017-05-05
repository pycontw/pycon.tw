import collections
import datetime

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

EVENTS_DAY_NAMES = collections.OrderedDict([
    (datetime.date(2016, 6, 3), _('Day 1')),
    (datetime.date(2016, 6, 4), _('Day 2')),
    (datetime.date(2016, 6, 5), _('Day 3')),
])
