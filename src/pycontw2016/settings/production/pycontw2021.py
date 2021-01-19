import os

from .base import BASE_DIR, STATICFILES_DIRS, TEMPLATES
from .base import *     # noqa

# Override static and media URL for prefix in WSGI server.
# https://code.djangoproject.com/ticket/25598
STATIC_URL = '/2021/static/'
MEDIA_URL = '/2021/media/'

CONFERENCE_DEFAULT_SLUG = 'pycontw-2021'
TEMPLATES[0]['DIRS'][1] = os.path.join(
    BASE_DIR, 'templates', CONFERENCE_DEFAULT_SLUG,
)
STATICFILES_DIRS[1] = os.path.join(
    BASE_DIR, 'static', CONFERENCE_DEFAULT_SLUG, '_includes',
)
