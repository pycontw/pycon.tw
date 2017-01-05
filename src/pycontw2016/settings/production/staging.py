from .base import *     # noqa

# Override static and media URL for prefix in WSGI server.
# https://code.djangoproject.com/ticket/25598
STATIC_URL = '/staging/static/'
MEDIA_URL = '/staging/media/'

CONFERENCE_DEFAULT_SLUG = 'pycontw-2017'
