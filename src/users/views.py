from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import ugettext
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from .decorators import login_forbidden
from .forms import UserCreationForm, UserProfileUpdateForm


User = get_user_model()


@sensitive_post_parameters()
@never_cache
@login_forbidden
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.send_activation_email(request)
            messages.success(request, ugettext(
                'An email has been sent to your email. Please follow '
                'instructions in the email to complete your signup.'
            ))
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@sensitive_post_parameters()
@never_cache
def user_activate(request, activation_key):
    # Always log the request out so the rest makes sense.
    if request.user.is_authenticated():
        logout(request)
    try:
        user = User.objects.get_with_activation_key(activation_key)
    except User.DoesNotExist:
        raise Http404
    user.is_active = True
    user.save()

    # HACK: By default Django requires password to log the user in. We circle
    # around it by marking it with the default backend, tricking Django into
    # thinking it as actually authenticated.
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    messages.success(request, ugettext(
        'Signup successful. You are now logged in.'
    ))
    return redirect('user_dashboard')


@login_required
def user_dashboard(request):
    logout_next = reverse('index')
    return render(request, 'users/user_dashboard.html', {
        'logout_next': logout_next,
    })


@login_required
def user_profile_update(request):
    logout_next = reverse('index')
    if request.method == 'POST':
        form = UserProfileUpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'users/user_profile_update.html', {
        'form': form, 'logout_next': logout_next,
    })
