"""
Django settings for pycontw2016 project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import collections
import datetime
import os

import environ
from django.conf import locale
from django.contrib.messages import constants as messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

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
                'core.context_processors.script_prefix',
                'core.context_processors.pycontw',
                'core.context_processors.frontend_host',
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

ALLOWED_HOSTS = ['0.0.0.0']

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': env.db_url(var='DATABASE_URL', default='postgres://postgres:secretpostgres@127.0.0.1:5432/pycontw2016'),
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
    'compressor_toolkit',
    'crispy_forms',
    'crispy_bootstrap3',
    'django_extensions',
    'import_export',
    'sorl.thumbnail',
    'registry',
    'corsheaders',
    'rest_framework'
)

LOCAL_APPS = (
    'core',
    'events',
    'proposals',
    'reviews',
    'sponsors',
    'users',
    'ccip',
    'attendee'
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
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'pycontw2016.urls'

WSGI_APPLICATION = 'pycontw2016.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

USE_I18N = True

USE_L10N = True

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('zh-hant', 'Traditional Chinese'),
    ('en-us', 'English (US)'),
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

COMPRESS_NODE_MODULES = os.path.join(os.path.dirname(BASE_DIR), 'node_modules')


def node_bin(name):
    return os.path.join(COMPRESS_NODE_MODULES, '.bin', name)


COMPRESS_BROWSERIFY_BIN = node_bin('browserify')

COMPRESS_ES6_COMPILER_CMD = (
    'export NODE_PATH="{paths}" && '
    '{browserify_bin} "{infile}" -o "{outfile}" '
    '-t [ '
    '"{node_modules}/babelify" '
    '--presets [ "@babel/preset-env" ] '
    '--plugins [ '
    '@babel/plugin-proposal-function-sent '
    '@babel/plugin-proposal-throw-expressions '
    '@babel/plugin-syntax-dynamic-import '
    '@babel/plugin-syntax-import-meta '
    '@babel/plugin-transform-class-properties ] '
    ']'
)

COMPRESS_NODE_SASS_BIN = node_bin('node-sass')

COMPRESS_POSTCSS_BIN = node_bin('postcss')

COMPRESS_SCSS_COMPILER_CMD = (
    '{node_sass_bin} --include --output-style expanded {paths} '
    '--include-path="{node_modules}" "{infile}" "{outfile}" && '
    '{postcss_bin} --use "{node_modules}/autoprefixer/lib/autoprefixer.js" '
    '--autoprefixer.browsers "{autoprefixer_browsers}" -r "{outfile}"'
)

COMPRESS_PRECOMPILERS = (
    ('module', 'compressor_toolkit.precompilers.ES6Compiler'),
    ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap3"

WERKZEUG_DEBUG = env.bool('WERKZEUG_DEBUG', default=True)

GTM_TRACK_ID = None

SLACK_WEBHOOK_URL = env.str('SLACK_WEBHOOK_URL', default=None)

IMPORT_EXPORT_USE_TRANSACTIONS = True

IMPORT_EXPORT_SKIP_ADMIN_LOG = True

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',
}


# Project settings.

CONFERENCE_CHOICES = [
    ('pycontw-2016', _('PyCon Taiwan 2016')),
    ('pycontw-2017', _('PyCon Taiwan 2017')),
    ('pycontw-2018', _('PyCon Taiwan 2018')),
    ('pycontw-2019', _('PyCon Taiwan 2019')),
    ('pycontw-2020', _('PyCon Taiwan 2020')),
    ('pycontw-2021', _('PyCon Taiwan 2021')),
    ('pycontw-2022', _('PyCon Taiwan 2022')),
    ('pycontw-2023', _('PyCon Taiwan 2023')),
    ('pycontw-2024', _('PyCon Taiwan 2024')),
    ('pycontw-2025', _('PyCon Taiwan 2025')),
]

CONFERENCE_DEFAULT_SLUG = 'pycontw-2025'
TEMPLATES[0]['DIRS'][1] = os.path.join(
    BASE_DIR, 'templates', CONFERENCE_DEFAULT_SLUG,
)
STATICFILES_DIRS[1] = os.path.join(
    BASE_DIR, 'static', CONFERENCE_DEFAULT_SLUG, '_includes',
)


TALK_PROPOSAL_DURATION_CHOICES = (
    ('NOPREF', _('No preference')),
    ('PREF15', _('Prefer 15min')),
    ('PREF30', _('Prefer 30min')),
)

EVENTS_DAY_NAMES = collections.OrderedDict([
    (datetime.date(2025, 9, 6), _('Day 1')),
    (datetime.date(2025, 9, 7), _('Day 2')),
])

COC_VERSION = '2024.0'

# Since 2021, pycon.tw has indivisual server hosting the attendee-facing pages
# (see the repo at https://github.com/pycontw/pycontw-2021) and this config
# provides the url hosting the frontend.
FRONTEND_HOST = 'https://staging.pycon.tw'
