import datetime

import pytest
from django.urls import reverse

from events.models import Location, ProposedTalkEvent, ProposedTutorialEvent, SponsoredEvent, Time


def test_sponsored_speech_list_fields_match_talk(
        api_client, accepted_talk_proposal, user):
    begin_time = Time.all_objects.create(
        value=datetime.datetime(2030, 1, 1, 1, tzinfo=datetime.timezone.utc),
    )
    sponsored_event = SponsoredEvent.objects.create(
        title="Sponsored talk",
        slug="sponsored-talk",
        host=user,
        category="NLP",
        language="ENEN",
        python_level="NOVICE",
        location=Location.R2,
        begin_time=begin_time,
    )
    talk_event = ProposedTalkEvent.objects.create(
        proposal=accepted_talk_proposal,
        location=sponsored_event.location,
        begin_time=sponsored_event.begin_time,
    )
    response = api_client.get('/api/events/speeches/', {"event_types": "talk,sponsored"})

    assert response.status_code == 200
    talk_data = next(
        event for event in response.json()
        if event["event_type"] == "talk" and event["id"] == talk_event.id
    )
    sponsored_data = next(
        event for event in response.json()
        if event["event_type"] == "sponsored" and event["id"] == sponsored_event.id
    )
    assert set(sponsored_data) == set(talk_data)
    assert sponsored_data["location"] == sponsored_event.location
    assert sponsored_data["begin_time"] == sponsored_event.begin_time_id.isoformat().replace('+00:00', 'Z')


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
