import pytest

from django.test import override_settings

from core.utils import collect_language_codes


@override_settings(
    LANGAUGES=[('en-us', 'English')],
    FALLBACK_LANGUAGE_PREFIXES={'en': 'en-us'},
)
def test_locale_fallback_middleware(client, settings):
    response = client.get('/en/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/', 302),
    ]


@override_settings(
    USE_I18N=False,
    LANGAUGES=[('en-us', 'English')],
    FALLBACK_LANGUAGE_PREFIXES={'en': 'en-us'},
)
def test_locale_fallback_middleware_no_i18n(client, settings):
    response = client.get('/en/')
    assert response.status_code == 404


@override_settings(LANGUAGE_CODE='en-us')
def test_collect_language_codes():
    assert collect_language_codes('zh-tw') == ['zh-tw', 'zh', 'en-us', 'en']
    assert collect_language_codes('zh') == ['zh', 'en-us', 'en']
    assert collect_language_codes('en-us') == ['en-us', 'en', 'en-us', 'en']
    assert collect_language_codes('en') == ['en', 'en-us', 'en']


def test_index_page(client):
    response = client.get('/en-us/')
    assert response.status_code == 200
    assert 'PyCon' in response.content.decode('utf-8')


@pytest.mark.parametrize('path,expected', [
    ('/en-us/speaking/cfp/',   200),
    ('/en-us/speaking/talk/',  200),
    ('/en-us/speaking/base/',  404),
    ('/en-us/speaking/_base/', 404),
])
def test_speaking_pages(client, path, expected):
    assert client.get(path).status_code == expected
