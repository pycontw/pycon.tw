from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import gettext
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST

from .decorators import login_forbidden
from .forms import (
    AuthenticationForm, PublicUserCreationForm, UserProfileUpdateForm,
    PasswordResetForm, SetPasswordForm,
)


User = get_user_model()


@sensitive_post_parameters()
@never_cache
@login_forbidden
def user_signup(request):
    if request.method == 'POST':
        form = PublicUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.send_verification_email(request)

            login(request, user)
            messages.success(request, gettext(
                'Sign up successful. You are now logged in.'
            ))
            return redirect('user_dashboard')
    else:
        form = PublicUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@sensitive_post_parameters()
@never_cache
def user_verify(request, verification_key):
    try:
        user = User.objects.get_with_verification_key(verification_key)
    except User.DoesNotExist:
        raise Http404
    user.verified = True
    user.save()
    messages.success(request, gettext('Email verification successful.'))
    return redirect('user_dashboard')


@never_cache
@login_required
@require_POST
def request_verification(request):
    user = request.user
    user.send_verification_email(request)
    messages.success(
        request,
        gettext('A verification email has been sent to {email}').format(
            email=user.email,
        ),
    )
    return redirect('user_dashboard')


@login_required
def user_dashboard(request):
    if not request.user.is_valid_speaker():
        return redirect('user_profile_update')
    logout_next = reverse('login')
    return render(request, 'users/user_dashboard.html', {
        'logout_next': logout_next,
    })


@login_required
def user_profile_update(request):
    logout_next = reverse('index')
    if request.method == 'POST':
        form = UserProfileUpdateForm(
            data=request.POST, files=request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, gettext(
                'Your profile has been updated successfully.',
            ))
            return redirect('user_dashboard')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'users/user_profile_update.html', {
        'form': form, 'logout_next': logout_next,
    })


def password_change_done(request):
    messages.success(request, gettext(
        'Your new password has been applied successfully.'
    ))
    return redirect('user_dashboard')


def password_reset_done(request):
    messages.success(request, gettext(
        'An email is sent to your email account. Please check your inbox for '
        'furthur instructions to reset your password.'
    ))
    return redirect('login')


def password_reset_complete(request):
    messages.success(request, gettext(
        'Password reset successful. You can now login.'
    ))
    return redirect('login')


def password_reset_confirm(request, uidb64, token):
    return base_password_reset_confirm(
        request, uidb64=uidb64, token=token,
        set_password_form=SetPasswordForm
    )
