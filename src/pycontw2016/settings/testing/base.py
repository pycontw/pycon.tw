import os

from ..local import BASE_DIR, STATICFILES_DIRS, TEMPLATES
from ..local import *   # noqa

DEBUG = False

LANGUAGE_CODE = 'en-us'

CONFERENCE_DEFAULT_SLUG = 'testing'
TEMPLATES[0]['DIRS'][1] = os.path.join(
    BASE_DIR, 'templates', CONFERENCE_DEFAULT_SLUG,
)
STATICFILES_DIRS[1] = os.path.join(
    BASE_DIR, 'static', CONFERENCE_DEFAULT_SLUG, '_includes',
)

EVENTS_PUBLISHED = True
