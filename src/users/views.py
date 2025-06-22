import lxml.html
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import get_language, gettext
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_GET, require_POST
from lxml import etree

from reviews.context import proposals_state, reviews_state

from .decorators import login_forbidden
from .forms import (
    AuthenticationForm,
    CocAgreementForm,
    PasswordResetForm,
    PublicUserCreationForm,
    SetPasswordForm,
    UserProfileUpdateForm,
)
from .models import CocRecord

User = auth.get_user_model()


@sensitive_post_parameters()
@never_cache
@login_forbidden
def user_signup(request):
    if request.method == 'POST':
        form = PublicUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.send_verification_email(request)

            auth.login(request, user)
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
    except User.DoesNotExist as err:
        raise Http404 from err
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
        **proposals_state()._asdict(),
        **reviews_state()._asdict(),
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
        **reviews_state()._asdict(),
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


@login_required
def coc_agree(request):
    if request.method == 'POST':
        form = CocAgreementForm(data=request.POST)
        if form.is_valid():
            try:
                agreement = CocRecord.objects.get(user=request.user, coc_version=settings.COC_VERSION)
            except CocRecord.DoesNotExist:
                agreement = CocRecord(user=request.user, coc_version=settings.COC_VERSION)

            agreement.save()

            # The query param indicating redirect target (setup by CocAgreementMixin) can be removed after set_language.
            # Redirect to dashboard intead if this situation happened.
            redirect_to = request.GET.get('next', reverse('user_dashboard'))
            return redirect(redirect_to)
    else:
        form = CocAgreementForm()

    # Get code of conduct
    lang = get_language()
    content = render_to_string('contents/%s/about/code-of-conduct.html' % lang[:2], {}, request)
    tree = lxml.html.document_fromstring(content)
    main = tree.xpath('//main')[0]

    # Remove the title
    # Since the HTML structure has changed
    # need to find the direct child from main which contains h1 as its descendant
    # and remove it
    for h1 in main.xpath('//h1'):
        target = h1
        parent = h1.getparent()

        while parent != main and parent is not None:
            target = parent
            parent = parent.getparent()

        if parent == main:
            main.remove(target)

    coc = etree.tostring(main, encoding='utf-8').decode('utf-8')

    return render(request, 'users/coc_agreement.html', {
        'form': form,
        'coc': coc,
        **reviews_state()._asdict(),
    })

@require_GET
def user_list(request):
    role = request.GET.get('role')
    qs = User.objects.all()
    if role:
        if not Group.objects.filter(name__iexact=role).exists():
            raise Http404(f"Group '{role}' does not exist.")
        qs = qs.filter(groups__name__iexact=role)
    users = []
    for user in qs:
        users.append({
            'email': user.email,
            'full_name': user.get_full_name(),
            'bio': user.bio,
            'photo_url': user.get_thumbnail_url(),
            'facebook_profile_url': user.facebook_profile_url,
            'twitter_profile_url': user.twitter_profile_url,
            'github_profile_url': user.github_profile_url,
            'verified': user.verified,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
        })
    return JsonResponse(list(users), safe=False)

class PasswordChangeView(auth_views.PasswordChangeView):
    # cannot merely pass extra_context=reviews_state()._asdict() to
    # auth_views.PasswordChangeView because
    # we need to resolve reviews_state()._asdict() everytime when
    # reaching this view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**reviews_state()._asdict())
        return context


login = auth_views.LoginView.as_view(authentication_form=AuthenticationForm)
logout = auth_views.LogoutView.as_view()
password_change = PasswordChangeView.as_view()
password_reset = auth_views.PasswordResetView.as_view(form_class=PasswordResetForm,
                                                      template_name='registration/password_reset.html',
                                                      email_template_name='registration/password_reset_email.txt')
password_reset_confirm = auth_views.PasswordResetConfirmView.as_view(
    form_class=SetPasswordForm
)
