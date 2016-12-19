import re

from django.conf import settings
from django.core.urlresolvers import get_script_prefix
from django.http import HttpResponseRedirect


# Matches things like
#   /en
#   /en/
#   /en/foo/bar (can be anything after the first trailing slash)
# But not
#   /en-gb
# because the fallback language code is not followed immediately by a slash.
FALLBACK_PREFIX_PATTERN = re.compile(
    r'^/(?P<lang>{langs})(?:/?|/.+)$'.format(
        langs='|'.join(settings.FALLBACK_LANGUAGE_PREFIXES.keys()),
    ),
    re.UNICODE,
)


class LocaleFallbackMiddleware(object):
    """Redirect entries in ``settings.FALLBACK_LANGUAGE_PREFIXES`` to a
    valid language prefix.
    """
    response_redirect_class = HttpResponseRedirect

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Return default response if USE_I18N is not enabled or if
        # FALLBACK_PREFIX_PATTERN does not match.
        if not settings.USE_I18N:
            return self.get_response(request)
        match = FALLBACK_PREFIX_PATTERN.match(request.path_info)
        if not match:
            return self.get_response(request)

        lang = match.group('lang')
        fallback = settings.FALLBACK_LANGUAGE_PREFIXES[lang]
        script_prefix = get_script_prefix()
        path = request.get_full_path().replace(
            script_prefix + lang, script_prefix + fallback, 1,
            )
        return self.response_redirect_class(path)
