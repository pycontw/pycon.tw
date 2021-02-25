import re

from django.template import Library


register = Library()


@register.filter
def message_bootstrap_class_str(message):
    return ' '.join('alert-' + tag for tag in message.tags.split(' '))


@register.filter
def get_path_category(url):
    pattern = r'/(?P<lang>zh\-hant|en\-us)/(?P<category>[0-9a-z-]*)/'
    result = re.search(pattern, url)
    if not result:
        return 'unmatched'
    return result.groupdict().get('category', 'uncategorized')
