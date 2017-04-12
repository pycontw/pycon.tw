"""
Django settings for pycontw2016 project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

import environ

from django.conf import locale
from django.contrib.messages import constants as messages
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, "directory")
BASE_DIR = os.path.abspath(os.path.join(__file__, '..', '..', '..'))

# Use Django templates using the new Django 1.8 TEMPLATES settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates', 'default'),
            os.path.join(BASE_DIR, 'templates', 'default'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'core.context_processors.google_analytics',
                'core.context_processors.proposals_states',
                'core.context_processors.reviews_states',
            ],
            'debug': True,
        },
    },
]

# Use 12factor inspired environment variables or from a file
env = environ.Env()

# Ideally move env file should be outside the git repo
# i.e. BASE_DIR.parent.parent
env_file = os.path.join(os.path.dirname(__file__), 'local.env')
if os.path.exists(env_file):
    environ.Env.read_env(str(env_file))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in
    # os.environ
    'default': env.db(),
}

# Application definition

DJANGO_APPS = (
    'modeltranslation',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'compressor',
    'crispy_forms',
    'django_extensions',
    'import_export',
)

LOCAL_APPS = (
    'core',
    'proposals',
    'users',
    'reviews',
    'events',
    'sponsors',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Enable Postgres-specific things if we are using it.
if 'postgres' in DATABASES['default']['ENGINE']:
    INSTALLED_APPS += ('postgres',)


MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'core.middlewares.LocaleFallbackMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pycontw2016.urls'

WSGI_APPLICATION = 'pycontw2016.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

USE_I18N = True

USE_L10N = True

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('zh-hant', 'Traditional Chinese'),
    ('en-us',   'English (US)'),
]

FALLBACK_LANGUAGE_PREFIXES = {
    'zh': 'zh-hant',
    'en': 'en-us',
}

if 'en-us' not in locale.LANG_INFO:
    locale.LANG_INFO['en-us'] = {
        'bidi': False,
        'code': 'en-us',
        'name': 'English (US)',
        'name_local': 'English (US)',
    }

# Path to the local .po and .mo files
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

USE_TZ = True

TIME_ZONE = 'Asia/Taipei'


# Message tag setup.
# https://docs.djangoproject.com/es/1.9/ref/contrib/messages/#message-tags

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'static', 'default', 'styles'),
]


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"

MEDIA_ROOT = env.str('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

MEDIA_URL = '/media/'

LIBSASS_SOURCEMAPS = True


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


# URL settings.

LOGIN_URL = reverse_lazy('login')

LOGOUT_URL = reverse_lazy('logout')

LOGIN_REDIRECT_URL = reverse_lazy('user_dashboard')


# Third-party app and custom settings.

AUTH_USER_MODEL = 'users.User'

ADMINS = (
    ('PyCon Taiwan Dev', 'dev@pycon.tw',),
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

WERKZEUG_DEBUG = env.bool('WERKZEUG_DEBUG', default=True)

GA_TRACK_ID = None

SLACK_WEBHOOK_URL = env.str('SLACK_WEBHOOK_URL', default=None)

IMPORT_EXPORT_USE_TRANSACTIONS = True

IMPORT_EXPORT_SKIP_ADMIN_LOG = True


# Project settings.

CONFERENCE_CHOICES = [
    ('pycontw-2016', _('PyCon Taiwan 2016')),
    ('pycontw-2017', _('PyCon Taiwan 2017')),
]

CONFERENCE_DEFAULT_SLUG = 'pycontw-2017'
TEMPLATES[0]['DIRS'][1] = os.path.join(
    BASE_DIR, 'templates', CONFERENCE_DEFAULT_SLUG,
)
STATICFILES_DIRS[1] = os.path.join(
    BASE_DIR, 'static', CONFERENCE_DEFAULT_SLUG, '_includes',
)

PROPOSALS_CREATABLE = False

PROPOSALS_EDITABLE = False

PROPOSALS_WITHDRAWABLE = False

REVIEWS_STAGE = 1

REVIEWS_VISIBLE_TO_SUBMITTERS = False

TALK_PROPOSAL_DURATION_CHOICES = (
    ('NOPREF', _('No preference')),
    ('PREF30', _('Prefer 30min')),
    ('PREF45', _('Prefer 45min')),
)
