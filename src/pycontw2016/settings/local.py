from .base import (
    BASE_DIR, INSTALLED_APPS, MIDDLEWARE, REVIEWS_STAGE,
    REVIEWS_VISIBLE_TO_SUBMITTERS,
    env,
)
from .base import *             # NOQA
import logging.config
import os
import sys


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Turn off debug while imported by Celery with a workaround
# See http://stackoverflow.com/a/4806384
if 'celery' in sys.argv[0]:
    DEBUG = False

# Django Debug Toolbar
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# Install local, development apps.
INSTALLED_APPS += env.tuple('LOCAL_APPS', default=())

# Show emails to console in DEBUG mode
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Log everything to the logs directory at the top
LOGFILE_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'logs')

# Reset logging
# http://www.caktusgroup.com/blog/2015/01/27/
# Django-Logging-Configuration-logging_config-default-settings-logger/

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
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname).1s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'django_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGFILE_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGFILE_ROOT, 'project.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django_log_file', 'console', ],
            'propagate': True,
            'level': 'DEBUG',
        },
        'project': {
            'handlers': ['proj_log_file', 'console', ],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['console'],
            'level': 0,
        },
    }
}

logging.config.dictConfig(LOGGING)


REVIEWS_STAGE = env.int('REVIEWS_STAGE', default=REVIEWS_STAGE)

REVIEWS_VISIBLE_TO_SUBMITTERS = env.bool(
    'REVIEWS_VISIBLE_TO_SUBMITTERS', default=REVIEWS_VISIBLE_TO_SUBMITTERS,
)

DJANGO_Q_DEBUG = True
