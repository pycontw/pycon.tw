from django.utils.translation import pgettext_lazy


SEP_DEFAULT = pgettext_lazy('speaker name default separator', ', ')
SEP_LAST = pgettext_lazy('speaker name last separator', ' and ')


def format_names(names, sep_default=SEP_DEFAULT, sep_last=SEP_LAST):
    assert names
    if len(names) == 1:
        return names[0]
    return '{}{}{}'.format(sep_default.join(names[:-1]), sep_last, names[-1])
