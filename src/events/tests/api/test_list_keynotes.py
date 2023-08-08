import pytest

from django.urls import reverse

from core.models import Token
from events.models import KeynoteEvent


@pytest.fixture
def keynote_param():
    return [
        "id",
        "speaker",
        "session",
        "slido",
        "hackmd_embed_link",
        "youtube_id",
        "social_item"
    ]


def test_list_keynotes(keynote_param, bare_user, drf_api_client):
    url = reverse("events:keynotes-list")
    token = Token.objects.get_or_create(user=bare_user)
    drf_api_client.credentials(HTTP_AUTHORIZATION=str(token[0]))
    response = drf_api_client.get(url)

    query = KeynoteEvent.objects.all()
    assert len(response.json()) == query.count()
    for event in response.json():
        assert list(event.keys()) == keynote_param

    assert response.status_code == 200
