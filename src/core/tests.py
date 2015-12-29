import pytest

from core.utils import collect_language_codes


def test_collect_language_codes():
    assert collect_language_codes('zh-tw') == ['zh-tw', 'zh', 'en']
    assert collect_language_codes('zh') == ['zh', 'en']
    assert collect_language_codes('en-uk') == ['en-uk', 'en', 'en']
    assert collect_language_codes('en') == ['en', 'en']


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
