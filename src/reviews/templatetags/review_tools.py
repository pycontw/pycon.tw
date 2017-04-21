import functools

from django.template import Library
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from core import difftools
from core.utils import html_join


register = Library()


def diff_tag(f):
    """Decorator that performs basic comparisons for a diff tag.
    """
    @functools.wraps(f)
    def inner(current, snapshot):
        if not snapshot or current == snapshot:
            return current
        return f(current, snapshot)

    return inner


@register.simple_tag
@diff_tag
def line_diff(current, snapshot):
    return format_html(
        '<ins>{current}</ins><br><del>{snapshot}</del>',
        current=current, snapshot=snapshot,
    )


@register.simple_tag
@diff_tag
def block_diff(current, snapshot):
    return html_join(mark_safe('<br>'), difftools.make_diff(
        current.splitlines(), snapshot.splitlines(),
    ))
