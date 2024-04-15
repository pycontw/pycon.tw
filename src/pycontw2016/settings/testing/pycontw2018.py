import os

from .base import *  # noqa
from .base import BASE_DIR, STATICFILES_DIRS, TEMPLATES

CONFERENCE_DEFAULT_SLUG = 'pycontw-2018'
TEMPLATES[0]['DIRS'][1] = os.path.join(BASE_DIR, 'templates', 'pycontw-2018')
STATICFILES_DIRS[1] = os.path.join(
    BASE_DIR, 'static', CONFERENCE_DEFAULT_SLUG, '_includes',
)

EVENTS_PUBLISHED = False
