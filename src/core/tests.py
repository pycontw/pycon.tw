import pytest

from django.test import override_settings

from core.utils import collect_language_codes


@override_settings(LANGUAGE_CODE='en-us')
def test_collect_language_codes():
    assert collect_language_codes('zh-tw') == ['zh-tw', 'zh', 'en-us', 'en']
    assert collect_language_codes('zh') == ['zh', 'en-us', 'en']
    assert collect_language_codes('en-gb') == ['en-gb', 'en', 'en-us', 'en']
    assert collect_language_codes('en') == ['en', 'en-us', 'en']


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'PyCon' in response.content.decode('utf-8')


@pytest.mark.parametrize('path,expected', [
    ('/speaking/cfp/',   200),
    ('/speaking/talk/',  200),
    ('/speaking/base/',  404),
    ('/speaking/_base/', 404),
])
def test_speaking_pages(client, path, expected):
    assert client.get(path).status_code == expected
