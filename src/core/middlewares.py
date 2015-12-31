import re

from django.conf import settings
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


class LocaleFallbackMiddleware:
    """Redirect entries in ``settings.FALLBACK_LANGUAGE_PREFIXES`` to a
    valid language prefix.
    """
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        if not settings.USE_I18N:
            return
        match = FALLBACK_PREFIX_PATTERN.match(request.path_info)
        if not match:
            return
        lang = match.group('lang')
        fallback = settings.FALLBACK_LANGUAGE_PREFIXES[lang]
        path = request.get_full_path().replace(lang, fallback, 1)
        return self.response_redirect_class(path)
