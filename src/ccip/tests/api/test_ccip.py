import pytest
from django.conf import settings

endpoint = "/ccip/"

def assert_data_structure(data, key):
    items = data.get(key, [])
    for item in items:
        assert 'id' in item
        assert 'zh' in item
        assert 'en' in item
        assert 'name' in item['zh']
        assert 'name' in item['en']

@pytest.mark.django_db
def test_data_structure(client):
    response = client.get(endpoint, follow=True)
    assert response.status_code == 200
    data = response.json()

    assert_data_structure(data, 'session_types')
    assert_data_structure(data, 'tags')
    assert_data_structure(data, 'rooms')
