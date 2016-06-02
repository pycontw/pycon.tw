from django.template import Library

from proposals.utils import SEP_DEFAULT, SEP_LAST, format_names


register = Library()


@register.filter
def speaker_names_display(
        proposal, sep_default=SEP_DEFAULT, sep_last=SEP_LAST):
    names = [info.user.speaker_name for info in proposal.speakers]
    return format_names(names, sep_default=sep_default, sep_last=sep_last)
