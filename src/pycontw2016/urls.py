from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.i18n import set_language

from core.views import error_page, flat_page, index
from users.views import user_dashboard


urlpatterns = i18n_patterns(

    # Add top-level URL patterns here.
    url(r'^$', index, name='index'),
    url(r'^dashboard/$', user_dashboard, name='user_dashboard'),
    url(r'^accounts/', include('users.urls')),
    # url(r'^conference/', include('events.urls')),
    url(r'^proposals/', include('proposals.urls')),
    url(r'^reviews/', include('reviews.urls')),
    # url(r'^ext/', include('ext2020.urls')),

    # Match everything except admin, media, static, and error pages.
    url(r'^(?!admin|api|{media}|{static}|404|500/)(?P<path>.*)/$'.format(
        media=settings.MEDIA_URL.strip('/'),
        static=settings.STATIC_URL.strip('/')),
        flat_page, name='page'),

    url(r'^(?P<code>404|500)/$', error_page),
)

# These should not be prefixed with language.
urlpatterns += [
    url(r'^ccip/', include('ccip.urls')),
    url(r'^api/sponsors/', include('sponsors.api.urls')),
    url(r'^api/events/', include('events.api.urls', namespace="events")),
    url(r'^set-language/$', set_language, name='set_language'),
    url(r'^admin/', admin.site.urls),
]

# User-uploaded files like profile pics need to be served in development.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug Toolbar's URL.
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
