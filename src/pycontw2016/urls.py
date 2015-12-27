from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from core.views import flat_page
from users.views import user_dashboard


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^dashboard/$', user_dashboard, name='user_dashboard'),
    url(r'^accounts/', include('users.urls')),
    url(r'^proposals/', include('proposals.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/$',
        TemplateView.as_view(template_name="change_lang.html"),
        name='change_lang'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

if settings.URL_PREFIX:
    urlpatterns = [
        url(r'^{prefix}'.format(prefix=settings.URL_PREFIX),
            include(urlpatterns)),
    ]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all URL pattern must be put last.
if settings.URL_PREFIX:
    urlpatterns += [
        url(r'^{prefix}(?P<path>.+)/$'.format(prefix=settings.URL_PREFIX),
            flat_page, name='page'),
    ]
else:
    urlpatterns += [url(r'^(?P<path>.+)/$', flat_page, name='page')]
