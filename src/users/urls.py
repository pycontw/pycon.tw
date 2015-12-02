from django.conf.urls import url
from django.contrib.auth import views as auth

from . import views


urlpatterns = [
    url(r'^login/$', auth.login, name='login'),
    url(r'^logout/$', auth.logout, name='logout'),
    url(r'^profile/$', views.user_profile_update, name='user_profile_update'),
    url(r'^signup/$', views.user_signup, name='signup'),
]
