from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy


def login_forbidden(function=None, redirect_url=None):
    """The reverse of ``login_required``.

    The requet is redirected to ``redirect_url`` (``user_dashboard`` by
    default) if the user is authenticated.
    """
    if redirect_url is None:
        # This needs to be reversed lazily so the decorator can decorate
        # views (which are loaded before URL names).
        redirect_url = reverse_lazy('user_dashboard')
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous(),
        login_url=redirect_url, redirect_field_name=None,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
