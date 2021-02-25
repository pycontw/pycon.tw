"""
WSGI config for pycontw2016 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""
import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'pycontw2016.settings.production.pycontw2016',
)
application = get_wsgi_application()

if settings.DEBUG:
    # Wrap werkzeug debugger.
    if settings.WERKZEUG_DEBUG:
        try:
            import django.views.debug
            import six
            from werkzeug.debug import DebuggedApplication
        except ImportError:
            pass
        else:
            def null_response(request, exc_type, exc_value, tb):
                six.reraise(exc_type, exc_value, tb)

            django.views.debug.technical_500_response = null_response
            application = DebuggedApplication(application, evalex=True)
else:
    # Wrap Sentry.
    try:
        from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
    except ImportError:
        pass
    else:
        application = Sentry(application)
