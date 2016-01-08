from django.conf.urls import url
from django.contrib.auth import views as auth

from . import views


urlpatterns = [

    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', auth.logout, name='logout'),
    url(r'^profile/$', views.user_profile_update, name='user_profile_update'),

    url(r'^password-change/$', auth.password_change, name='password_change'),
    url(r'^password-change/done/$',
        views.password_change_done, name='password_change_done'),

    url(r'^signup/$',
        views.user_signup, name='signup'),
    url(r'^verify/(?P<verification_key>[-:\w]+)/$',
        views.user_verify, name='user_verify'),
    url(r'^verification-request/$',
        views.request_verification, name='request_verification'),

    url(r'^password-reset/$',
        views.password_reset, name='password_reset'),
    url(r'^password-reset/done/$',
        views.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        views.password_reset_complete, name='password_reset_complete'),

]
