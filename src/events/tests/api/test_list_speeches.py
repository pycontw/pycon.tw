import pytest

from django.urls import reverse

from core.models import Token
from events.models import (
    ProposedTalkEvent, ProposedTutorialEvent, SponsoredEvent,
)


@pytest.mark.parametrize(
    "category",
    [
        "WEB",
        "EMBED",
        "ADMIN",
        "OTHER",
        "TOOL",
        "ML",
        "LIBS",
        "GAME",
        "SCI",
        "APPL",
        "PRAC",
        "COM",
        "GRAPH",
        "CORE",
        "IOT",
        "SEC",
        "EDU",
        "NLP",
        "DATA",
        "DB",
        "FIN",
        "TEST",
        "WEB",
        "INTNL",
    ],
)
def test_list_speeches_by_category(category, bare_user, drf_api_client):
    url = reverse("events:speeches-category", kwargs={"category": category})
    token = Token.objects.get_or_create(user=bare_user)
    drf_api_client.credentials(HTTP_AUTHORIZATION=str(token[0]))
    response = drf_api_client.get(url)

    for event in response.json():
        assert event["category"] == category

    assert (
        len(response.json()) == ProposedTalkEvent.objects.filter(proposal__category=category).count() +
        ProposedTutorialEvent.objects.filter(proposal__category=category).count() +
        SponsoredEvent.objects.filter(category=category).count()
    )

    assert response.status_code == 200


@pytest.mark.parametrize(
    "event_type",
    [
        "talk",
        "sponsored",
        "tutorial"
    ],
)
@pytest.mark.parametrize(
    "category",
    [
        "WEB",
        "EMBED",
        "ADMIN",
        "OTHER",
        "TOOL",
        "ML",
        "LIBS",
        "GAME",
        "SCI",
        "APPL",
        "PRAC",
        "COM",
        "GRAPH",
        "CORE",
        "IOT",
        "SEC",
        "EDU",
        "NLP",
        "DATA",
        "DB",
        "FIN",
        "TEST",
        "WEB",
        "INTNL",
    ],
)
def test_list_speeches(category, event_type, bare_user, drf_api_client):
    url = reverse("events:speeches-list")
    token = Token.objects.get_or_create(user=bare_user)
    drf_api_client.credentials(HTTP_AUTHORIZATION=str(token[0]))
    response = drf_api_client.get(url)

    for event in response.json():
        assert event["event_type"] == event_type

    assert (
        len(response.json()) == ProposedTalkEvent.objects.filter(proposal__category=category).count() +
        ProposedTutorialEvent.objects.filter(proposal__category=category).count() +
        SponsoredEvent.objects.filter(category=category).count()
    )

    assert response.status_code == 200


@pytest.fixture
def talk():
    return [
        'id',
        'begin_time',
        'end_time',
        'is_remote',
        'location',
        'youtube_id',
        'title',
        'category',
        'language',
        'python_level',
        'recording_policy',
        'abstract',
        'detailed_description',
        'slide_link',
        'slido_embed_link',
        'hackmd_embed_link',
        'speakers',
        'event_type'
    ]


@pytest.fixture
def sponsored():
    return [
        "id", "title", "category", "language", "python_level",
        "recording_policy", "abstract", "detailed_description",
        "slide_link", "slido_embed_link", "hackmd_embed_link",
        "speakers", "location", "begin_time", "end_time",
        "event_type", 'youtube_id'
    ]


@pytest.fixture
def tutorial():
    return [
        'id',
        'begin_time',
        'end_time',
        'is_remote',
        'location',
        'registration_link',
        'youtube_id',
        'title',
        'category',
        'language',
        'python_level',
        'recording_policy',
        'abstract',
        'detailed_description',
        'slide_link',
        'slido_embed_link',
        'hackmd_embed_link',
        'speakers',
        'event_type'
    ]


@pytest.mark.parametrize(
    "event_type",
    [
        'talk',
        'sponsored',
        'tutorial'
    ]
)
def test_detail_speeches(event_type, talk, sponsored, tutorial, bare_user, drf_api_client):
    if event_type == 'talk':
        url = reverse("events:speeches-event_type", kwargs={"event_type": event_type, "pk": '286'})
    elif event_type == 'sponsored':
        url = reverse("events:speeches-event_type", kwargs={"event_type": event_type, "pk": '9999'})
    else:
        url = reverse("events:speeches-event_type", kwargs={"event_type": event_type, "pk": '15'})
    token = Token.objects.get_or_create(user=bare_user)
    drf_api_client.credentials(HTTP_AUTHORIZATION=str(token[0]))
    response = drf_api_client.get(url)

    for event in response.json():
        assert event["event_type"] == event_type
        if event_type == 'talk':
            assert list(response.json().keys()) == talk
        elif event_type == 'sponsored':
            assert list(response.json().keys()) == sponsored
        else:
            assert list(response.json().keys()) == tutorial
    assert response.status_code == 200
