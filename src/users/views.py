from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from .decorators import login_forbidden
from .forms import UserCreationForm, UserProfileUpdateForm


@sensitive_post_parameters()
@never_cache
@login_forbidden
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(authenticated=True)
            # TODO: Send an email to notify the email owner that the email is
            # used for registration. Don't need to verify, but need to be
            # notified (and let the owner do something if this is a mistake).
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


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
