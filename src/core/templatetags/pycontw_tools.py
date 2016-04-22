from django.template import Library


register = Library()


@register.filter
def message_bootstrap_class_str(message):
    return ' '.join('alert-' + tag for tag in message.tags.split(' '))
