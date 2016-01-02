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

    url(r'^signup/$', views.user_signup, name='signup'),
    url(r'^verify/(?P<verification_key>[-:\w]+)/$',
        views.user_verify, name='user_verify'),
    url(r'^verification-request/$',
        views.request_verification, name='request_verification'),
]
