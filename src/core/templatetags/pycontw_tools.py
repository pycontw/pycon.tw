import re

from django.template import Library


register = Library()


@register.filter
def message_bootstrap_class_str(message):
    return ' '.join('alert-' + tag for tag in message.tags.split(' '))


@register.filter
def get_path_category(url):
    lang = '\/(zh\-hant|en\-us)'
    category_pattern_mapping = {
        'about': '\/about/pycontw',
        'sponsor': '\/sponsor/sponsor',
        'speaking': '\/speaking\/(cfp|talk|tutorial|recording)',
        'conference': '\/(events\/(overview|schedule)|portal)',
        'event': '\/events\/(keynotes|talks|open-spaces)',
        'registration': '\/registration/(financial-aid|ticket-info|registration)',
        'venue': '\/venue'
    }
    end = '\/?$'
    for category, pattern in category_pattern_mapping.items():
        if re.match(lang + pattern + end, url):
            return category
    return 'uncategorized'
