from django.test import override_settings


def test_locale_fallback_middleware(client, settings):
    response = client.get('/en/', follow=True)
    assert response.redirect_chain == [('/en-us/', 302)]


@override_settings(USE_I18N=False)
def test_locale_fallback_middleware_no_i18n(client, settings):
    response = client.get('/en/')
    assert response.status_code == 404
