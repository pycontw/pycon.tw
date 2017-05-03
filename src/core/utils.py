import collections

from django.conf import settings
from django.http import Http404
from django.template.loader import TemplateDoesNotExist
from django.template.response import TemplateResponse
from django.utils.functional import lazy
from django.utils.html import conditional_escape, format_html, mark_safe


format_html_lazy = lazy(format_html, str)


def html_join(sep, sequence):
    """Similar to str.join, but passes the separator and all elements in the
    sequence through conditional_escape, and calls 'mark_safe' on the result.
    This function should be used instead of str.join to build up small HTML
    fragments.
    """
    sep_safe = conditional_escape(sep)
    return mark_safe(sep_safe.join(conditional_escape(e) for e in sequence))


class TemplateExistanceStatusResponse(TemplateResponse):
    """Extended response that raises Http404 when a template cannot be found.
    """
    def resolve_template(self, template):
        try:
            return super().resolve_template(template)
        except (UnicodeEncodeError, TemplateDoesNotExist):
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


class OrderedDefaultDict(collections.OrderedDict):
    """Marriage between OrderedDict and defaultdict.
    """
    def __init__(self, default_factory=None, *args, **kwargs):
        if default_factory is not None and not callable(default_factory):
            raise TypeError('first argument must be callable')
        super().__init__(*args, **kwargs)
        self.default_factory = default_factory

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key,)
        result = self[key] = self.default_factory()
        return result
