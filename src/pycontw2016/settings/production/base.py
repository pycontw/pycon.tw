"""In production set the environment variable like this::

    DJANGO_SETTINGS_MODULE=my_proj.settings.production
"""

from ..base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE, TEMPLATES, env
from ..base import *            # noqa

import logging.config
import os

# For security and performance reasons, DEBUG is turned off
DEBUG = False

# Must mention ALLOWED_HOSTS in production!
ALLOWED_HOSTS = ['tw.pycon.org']

# Cache the templates in memory for speed-up
TEMPLATES[0]['OPTIONS'].update({"loaders": [
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
    ),
]})
TEMPLATES[0]['OPTIONS'].update({"debug": False})
if 'APP_DIRS' in TEMPLATES[0]:
    del TEMPLATES[0]['APP_DIRS']

# Explicitly tell Django where to find translations.
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# Log everything to the logs directory at the top
LOGFILE_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'logs')

# Reset logging
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '[%(asctime)s] %(levelname)s '
                '[%(pathname)s:%(lineno)s] %(message)s'
            ),
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGFILE_ROOT, 'project.log'),
            'formatter': 'verbose'
        },
        'django_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGFILE_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django_log_file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'project': {
            'handlers': ['proj_log_file'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING)

MIDDLEWARE += (
    'raven.contrib.django.raven_compat.middleware.'
    'SentryResponseErrorIdMiddleware',
)

EMAIL_BACKEND = env.email_url()['EMAIL_BACKEND']
EMAIL_HOST = env.email_url()['EMAIL_HOST']
EMAIL_HOST_PASSWORD = env.email_url()['EMAIL_HOST_PASSWORD']
EMAIL_HOST_USER = env.email_url()['EMAIL_HOST_USER']
EMAIL_PORT = env.email_url()['EMAIL_PORT']
EMAIL_USE_TLS = env.email_url()['EMAIL_USE_TLS']

DEFAULT_FROM_EMAIL = SERVER_EMAIL = '{name} <{addr}>'.format(
    name='PyCon Taiwan',
    addr='web@pycon.tw',
)

# Securiy related settings
SECURE_HSTS_SECONDS = 2592000
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'DENY'


# Setting for sentry

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

import raven    # noqa

RAVEN_CONFIG = {
    'dsn': env('DSN_URL'),
    'release': raven.fetch_git_sha(os.path.dirname(BASE_DIR)),
}

GTM_TRACK_ID = env('GTM_TRACK_ID', default=None)

DJANGO_Q_DEBUG = False
