import pytest

from django.urls import reverse

from core.models import Token
from events.models import ProposedTalkEvent, ProposedTutorialEvent, SponsoredEvent


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
