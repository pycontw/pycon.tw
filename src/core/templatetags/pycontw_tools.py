from django.template import Library
from django.utils.translation import pgettext_lazy


register = Library()


@register.filter
def message_bootstrap_class_str(message):
    return ' '.join('alert-' + tag for tag in message.tags.split(' '))


@register.filter
def speaker_names_display(
        proposal,
        sep_default=pgettext_lazy('speaker name default separator', ', '),
        sep_last=pgettext_lazy('speaker name last separator', ' and ')):
    names = [info.user.speaker_name for info in proposal.speakers]
    assert names
    if len(names) == 1:
        return names[0]
    return '{}{}{}'.format(sep_default.join(names[:-1]), sep_last, names[-1])
