from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.i18n import set_language

from core.views import flat_page, index
from users.views import user_dashboard


# Match everything except those starting with MEDIA_URL or STATIC_URL.
NONASSETS_PATTERN = r'^(?!{media}|{static}/)(?P<path>.*)/$'.format(
    media=settings.MEDIA_URL.strip('/'),
    static=settings.STATIC_URL.strip('/'),
)


# Add top-level URL patterns here.
urlpatterns = i18n_patterns(
    url(r'^$', index, name='index'),
    url(r'^dashboard/$', user_dashboard, name='user_dashboard'),
    url(r'^accounts/', include('users.urls')),
    url(r'^proposals/', include('proposals.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(NONASSETS_PATTERN, flat_page, name='page'),
) + [
    url(r'^set-language/$', set_language, name='set_language'),
]


# Prepend URL prefix if needed.
if settings.URL_PREFIX:
    urlpatterns = [
        url(r'^{prefix}'.format(prefix=settings.URL_PREFIX),
            include(urlpatterns)),
    ]


# User-uploaded files like profile pics need to be served in development.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
