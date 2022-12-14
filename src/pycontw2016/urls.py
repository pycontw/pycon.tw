from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.i18n import set_language
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core.views import error_page, flat_page, index
from users.views import user_dashboard


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = i18n_patterns(

    # Add top-level URL patterns here.
    url(r'^$', index, name='index'),
    url(r'^dashboard/$', user_dashboard, name='user_dashboard'),
    url(r'^accounts/', include('users.urls')),
    # url(r'^conference/', include('events.urls')),
    url(r'^proposals/', include('proposals.urls')),
    url(r'^reviews/', include('reviews.urls')),

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
    url(r'^api/attendee/', include('attendee.api.urls'))
]

# User-uploaded files like profile pics need to be served in development.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug Toolbar's URL.
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += [
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
