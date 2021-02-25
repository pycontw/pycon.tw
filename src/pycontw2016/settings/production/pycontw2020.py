import os

from .base import BASE_DIR, STATICFILES_DIRS, TEMPLATES
from .base import *     # noqa

# Override static and media URL for prefix in WSGI server.
# https://code.djangoproject.com/ticket/25598
STATIC_URL = '/2020/static/'
MEDIA_URL = '/2020/media/'

CONFERENCE_DEFAULT_SLUG = 'pycontw-2020'
TEMPLATES[0]['DIRS'][1] = os.path.join(
    BASE_DIR, 'templates', CONFERENCE_DEFAULT_SLUG,
)
STATICFILES_DIRS[1] = os.path.join(
    BASE_DIR, 'static', CONFERENCE_DEFAULT_SLUG, '_includes',
)

SCHEDULE_REDIRECT_URL = 'https://docs.google.com/spreadsheets/d/1efjxIesuNWaXBPwnaM8XPNpVF9Fo6dStGDjXVNG8AVo'
