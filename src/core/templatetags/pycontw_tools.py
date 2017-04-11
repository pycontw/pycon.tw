from django.template import Library


register = Library()


@register.filter
def mul(value, arg):
    return value * arg


@register.filter
def message_bootstrap_class_str(message):
    return ' '.join('alert-' + tag for tag in message.tags.split(' '))
