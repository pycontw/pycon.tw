from django.template import Library


register = Library()


@register.filter
def language_code(language):
    """Work around Django's non-standard locale recognition.

    Django describes en-us as simply en, which causes problems if we do use
    the standard en-us locale. We work around this problem by overriding the
    "en" output with "en-us".
    """
    code = language['code']
    if code == 'en':
        return 'en-us'
    return code


@register.filter
def language_name_local(language):
    """Work around Django's non-standard locale recognition.

    Django describes en-us as simply en, which causes problems if we do use
    the standard en-us locale. We work around this problem by overriding the
    "English" with "English (United States)".
    """
    name_local = language['name_local']
    if name_local == 'English':
        return 'English (Unites States)'
    return name_local
