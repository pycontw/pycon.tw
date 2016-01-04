from django.forms.widgets import flatatt
from django.template import Library


register = Library()


@register.inclusion_tag('_includes/character_counter.html')
def character_counter(source_id, min=None, max=None, extra_classes=None):
    attrs = {'data-source-id': source_id, 'class': 'character-count-display'}
    if min is not None:
        attrs['data-limit-min'] = min
    if max is not None:
        attrs['data-limit-max'] = max
    return {
        'attrs': flatatt(attrs),
        'class': ' '.join(['character-counter'] + (extra_classes or [])),
    }
