from django.template import Library
from django.utils.html import format_html


register = Library()


def _get(obj, field_name):
    value = getattr(obj, field_name)
    return value() if callable(value) else value


@register.simple_tag
def line_diff(current, snapshot, field_name):
    current = _get(current, field_name)
    if not snapshot:
        return current
    snapped = _get(snapshot, field_name)
    if current == snapped or not snapped:
        return current
    return format_html(
        '<ins>{current}</ins><br><del>{snapped}</del>',
        snapped=snapped, current=current,
    )


@register.simple_tag
def block_diff():
    return ''
