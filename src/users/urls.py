from django.conf.urls import url
from django.contrib.auth import views as auth

from .forms import (
    AuthenticationForm, PublicUserCreationForm, UserProfileUpdateForm,
    PasswordResetForm, SetPasswordForm,
)

from . import views


urlpatterns = [

    url(r'^login/$', 
        auth.LoginView.as_view(authentication_form=AuthenticationForm), name='login'),
    url(r'^logout/$', auth.LogoutView.as_view(), name='logout'),
    url(r'^profile/$', views.user_profile_update, name='user_profile_update'),

    url(r'^password-change/$', auth.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password-change/done/$',
        views.password_change_done, name='password_change_done'),

    url(r'^signup/$',
        views.user_signup, name='signup'),
    url(r'^verify/(?P<verification_key>[-:\w]+)/$',
        views.user_verify, name='user_verify'),
    url(r'^verification-request/$',
        views.request_verification, name='request_verification'),

    url(r'^password-reset/$',
        auth.PasswordResetView.as_view(form_class=PasswordResetForm,
                                       template_name='registration/password_reset.html',
                                       email_template_name='registration/password_reset_email.txt'),
        name='password_reset'),
    url(r'^password-reset/done/$',
        views.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth.PasswordResetConfirmView.as_view(form_class=SetPasswordForm),
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        views.password_reset_complete, name='password_reset_complete'),

]
