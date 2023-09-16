import pytest
from django.conf import settings

endpoint = "/ccip/"


@pytest.mark.django_db
def test_(client):
    response = client.get(endpoint, follow=True)
    assert response.status_code == 200
    data = response.json()
    assert 'rooms' in data
    rooms = data['rooms']
    for room in rooms:
        assert 'id' in room
        assert 'zh' in room
        assert 'en' in room

@pytest.mark.django_db
def test_session_types(client):
    response = client.get(endpoint, follow=True)
    assert response.status_code == 200
    expected_session_types = [
        {
            "id": "event",
            "zh": {
                "name": "活動"
            },
            "en": {
                "name": "event"
            }
        },
        {
            "id": "break",
            "zh": {
                "name": "休息"
            },
            "en": {
                "name": "break"
            }
        },
        {
            "id": "keynote",
            "zh": {
                "name": "基調演講"
            },
            "en": {
                "name": "keynote"
            }
        },
        {
            "id": "sponsored",
            "zh": {
                "name": "贊助"
            },
            "en": {
                "name": "sponsored"
            }
        },
        {
            "id": "tutorial",
            "zh": {
                "name": "專業課程"
            },
            "en": {
                "name": "tutorial"
            }
        },
        {
            "id": "talk",
            "zh": {
                "name": "演講"
            },
            "en": {
                "name": "talk"
            }
        }
    ]
    data = response.json()
    assert 'session_types' in data
    assert data['session_types'] == expected_session_types

