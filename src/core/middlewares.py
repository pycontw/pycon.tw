import re

from django.conf import settings
from django.http import HttpResponseRedirect


FALLBACK_PREFIX_PATTERN = re.compile(
    r'^/(?P<lang>{langs})/'.format(
        langs='|'.join(settings.FALLBACK_LANGUAGE_PREFIXES),
    ),
    re.UNICODE,
)


class LenientLocaleFallbackMiddleware:
    """Redirect entries in ``settings.FALLBACK_LANGUAGE_PREFIXES`` to a
    valid language prefix.
    """
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        match = FALLBACK_PREFIX_PATTERN.match(request.path_info)
        if not match:
            return
        lang = match.group('lang')
        fallback = settings.FALLBACK_LANGUAGE_PREFIXES[lang]
        path = request.get_full_path().replace(lang, fallback, 1)
        return self.response_redirect_class(path)
