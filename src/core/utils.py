import collections
import datetime

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
    a fallback. The site's default langauge (``settings.LANGUAGE_CODE``),
    its base language (if applicable), and a default directory "_default" are
    then appended as further fallbacks.

    Examples (assuming site language is "en"):

    * "zh-tw" -> "zh-tw", "zh", "en", "_default"
    * "ja"    -> "ja", "en", "_default"

    :returns: An ordered iterable containing collected language codes.
    """
    codes = [user_code]
    if '-' in user_code:
        codes.append(user_code.split('-')[0])
    codes.append(settings.LANGUAGE_CODE)
    if '-' in settings.LANGUAGE_CODE:
        codes.append(settings.LANGUAGE_CODE.split('-')[0])
    codes.append('_default')
    return codes


def form_has_instance(form):
    instance = getattr(form, 'instance', None)
    return instance and instance.pk is not None


def split_css_class(class_str):
    if not class_str:
        return set()
    return set(s.strip() for s in class_str.split())


class SequenceQuerySet:
    """Wrap a sequence to use the same API as Django's QuerySet.
    """
    __slots__ = ('_seq')

    def __init__(self, seq):
        self._seq = seq

    def __repr__(self):
        return '<SequenceQuerySet: {seq!r}>'.format(seq=self._seq)

    def __len__(self):
        return len(self._seq)

    def __iter__(self):
        return iter(self._seq)

    def __bool__(self):
        return bool(self._seq)

    def __getitem__(self, i):
        return type(self)(self._seq[i])

    def all(self):
        return self

    def count(self):
        return len(self._seq)

    def exists(self):
        return bool(self._seq)


TimeRange = collections.namedtuple('TimeRange', 'start end')
"""Represents a range between `datetime.time` instances `[start, end)`.
"""


def time_add(date, time, delta):
    """Apply `datetime.timedelta` to a `datetime.time` instance on a given
    `datetime.date`.
    """
    dt = datetime.datetime.combine(date, time)
    dt = dt + delta
    return dt.time()
