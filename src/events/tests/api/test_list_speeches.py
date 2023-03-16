import pytest
from django.urls import reverse

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
def test_list_speeches_by_category(category, api_client):
    url = reverse("events:speeches-category", kwargs={"category": category})
    response = api_client.get(url)

    for event in response.json():
        assert event["category"] == category

    assert (
        len(response.json()) == ProposedTalkEvent.objects.filter(proposal__category=category).count() +
        ProposedTutorialEvent.objects.filter(proposal__category=category).count() +
        SponsoredEvent.objects.filter(category=category).count()
    )

    assert response.status_code == 200
