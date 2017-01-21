from django.core.urlresolvers import get_script_prefix
from django.template import Library


register = Library()


@register.filter
def language_free_path(request):
    script_prefix = get_script_prefix()
    path_prefix = script_prefix + request.LANGUAGE_CODE + '/'
    path = request.path
    if path.startswith(path_prefix):
        path = path.replace(path_prefix, script_prefix, 1)
    return path


@register.filter
def path_for_language(request, language_code):
    script_prefix = get_script_prefix()
    path = request.path
    path_prefix = script_prefix + request.LANGUAGE_CODE + '/'
    i18n_prefix = script_prefix + language_code + '/'
    if path.startswith(path_prefix):
        path = path.replace(path_prefix, i18n_prefix, 1)
    else:
        path = path.replace(script_prefix, i18n_prefix, 1)
    return path
