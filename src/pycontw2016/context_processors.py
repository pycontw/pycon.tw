import re


def i18n(request):
    """Extract the non-i18n part from the current path.

    If the current locale is found at the beginning of the path, the path
    *without* the prefix will be returned. If the locale name is not found,
    the current path is used.

    For ease of use in templates, leading and trailing slashes are removed
    from the returned string.
    """
    path = request.path.strip('/')
    match = re.match(r'{}/?(.*)$'.format(request.LANGUAGE_CODE), path)
    if match:
        path = match.group(1)
    return {'i18n_path': path}
