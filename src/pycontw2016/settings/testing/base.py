import os

from ..local import BASE_DIR, TEMPLATES
from ..local import *   # noqa

DEBUG = False

LANGUAGE_CODE = 'en-us'

CONFERENCE_DEFAULT_SLUG = 'testing'
TEMPLATES[0]['DIRS'][1] = os.path.join(BASE_DIR, 'templates', 'testing')

EVENTS_PUBLISHED = True
