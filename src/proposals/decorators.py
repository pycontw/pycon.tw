from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def user_profile_required(function):
    """Decorator for views that checks if a user has a valid speaker profile.

    ``PermissionDenied`` is raised for users that do not have a valid speaker
    profile. Note that an anonymous user will also raise the exception; if you
    want to provide a chance to log in first, you can decorate the view with
    ``login_required`` first, like this::

        @user_profile_required
        @login_required
        def view_function(request):
            # ...
    """
    def check_profile(user):
        if user.is_anonymous() or not user.profile_filled:
            raise PermissionDenied
        return True

    actual_decorator = user_passes_test(
        check_profile,
        login_url=None, redirect_field_name=None,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
