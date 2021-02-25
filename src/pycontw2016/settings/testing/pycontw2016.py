import os

from .base import BASE_DIR, STATICFILES_DIRS, TEMPLATES
from .base import *     # noqa


CONFERENCE_DEFAULT_SLUG = 'pycontw-2016'
TEMPLATES[0]['DIRS'][1] = os.path.join(BASE_DIR, 'templates', 'pycontw-2016')
STATICFILES_DIRS[1] = os.path.join(
    BASE_DIR, 'static', CONFERENCE_DEFAULT_SLUG, '_includes',
)
