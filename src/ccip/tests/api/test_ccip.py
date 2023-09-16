import pytest
from django.conf import settings

endpoint = "/ccip/"

def assert_data_structure(data, key):
    assert key in data
    items = data.get(key, [])
    for item in items:
        assert 'id' in item
        assert 'zh' in item
        assert 'en' in item
        assert 'name' in item['zh']
        assert 'name' in item['en']
        if key == "speakers":
            assert 'avatar' in item
            assert 'bio' in item['zh']
            assert 'bio' in item['en']

@pytest.mark.django_db
def test_data_structure(client):
    response = client.get(endpoint, follow=True)
    assert response.status_code == 200
    data = response.json()

    assert_data_structure(data, 'session_types')
    assert_data_structure(data, 'tags')
    assert_data_structure(data, 'rooms')
    assert_data_structure(data, 'speakers')

@pytest.mark.django_db
def test_session(client):
    response = client.get(endpoint, follow=True)
    data = response.json()
    assert 'sessions' in data
    sessions = data.get('sessions', [])
    # 檢查每個 session 是否包含所需的字段
    required_fields = [
        "id", "type", "start", "end", "slide", "speakers", "tags",
        "en", "zh", "room", "broadcast", "qa", "live", "record"
    ]
    for session in sessions:
        for field in required_fields:
            assert field in session
        assert 'title' in session['en']
        assert 'description' in session['en']
        assert 'title' in session['zh']
        assert 'description' in session['zh']
