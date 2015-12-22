import pytest


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
