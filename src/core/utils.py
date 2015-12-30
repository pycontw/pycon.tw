from django.conf import settings
from django.http import Http404
from django.template.loader import TemplateDoesNotExist
from django.template.response import TemplateResponse
from django.utils.functional import lazy
from django.utils.html import format_html


format_html_lazy = lazy(format_html, str)


class TemplateExistanceStatusResponse(TemplateResponse):
    """Extended response that raises Http404 when a template cannot be found.
    """
    def resolve_template(self, template):
        try:
            return super().resolve_template(template)
        except TemplateDoesNotExist:
            raise Http404


def collect_language_codes(user_code):
    """Collect implied language codes for a requested langauge code.

    The language code requested is the first choice. If the code indicates a
    sublanguage (e.g. ``zh-hant``), the base language (``zh``) is collected as
    a fallback. The site's default langauge (``settings.LANGUAGE_CODE``) and
    its base language (if applicable) are then appended as further fallbacks.

    Examples (assuming site language is "en"):

    * "zh-tw" -> "zh-tw", "zh", "en"
    * "ja"    -> "ja", "en"

    :returns: An ordered iterable containing collected language codes.
    """
    codes = [user_code]
    if '-' in user_code:
        codes.append(user_code.split('-')[0])
    codes.append(settings.LANGUAGE_CODE)
    if '-' in settings.LANGUAGE_CODE:
        codes.append(settings.LANGUAGE_CODE.split('-')[0])
    return codes
