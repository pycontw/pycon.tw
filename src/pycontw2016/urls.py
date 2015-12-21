from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from users.views import user_dashboard

speaking_urlpatterns = [
    url('^cfp/$',
        TemplateView.as_view(template_name="speaking/cfp.html"),
        name='speaking_cfp'),
    url('^talk/$',
        TemplateView.as_view(template_name="speaking/talk.html"),
        name='speaking_talk'),
    url('^tutorial/$',
        TemplateView.as_view(template_name="speaking/tutorial.html"),
        name='speaking_tutorial'),
    url('^recording/$',
        TemplateView.as_view(template_name="speaking/recording.html"),
        name='speaking_recording'),
]

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^dashboard/$', user_dashboard, name='user_dashboard'),
    url(r'^accounts/', include('users.urls')),
    url(r'^proposals/', include('proposals.urls')),
    url(r'^speaking/', include(speaking_urlpatterns)),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.URL_PREFIX:
    urlpatterns = [
        url(r'^{prefix}'.format(prefix=settings.URL_PREFIX),
            include(urlpatterns)),
    ]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
