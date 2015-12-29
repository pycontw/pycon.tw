import re

from django.conf import settings
from django.http import HttpResponseRedirect


FALLBACK_LANGUAGE_PATTERN = re.compile(
    r'^/(?P<lang>{langs})/'.format(
        langs='|'.join(settings.FALLBACK_LANGUAGES),
    ),
    re.UNICODE,
)


class LenientLocaleFallbackMiddleware:
    """Redirect language prefixes in ``settings.FALLBACK_LANGUAGES`` to
    a valid language code.
    """
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        match = FALLBACK_LANGUAGE_PATTERN.match(request.path_info)
        if not match:
            return
        lang = match.group('lang')
        fallback = settings.FALLBACK_LANGUAGES[lang]
        path = request.get_full_path().replace(lang, fallback, 1)
        return self.response_redirect_class(path)
