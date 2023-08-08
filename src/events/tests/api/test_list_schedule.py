import pytest

from django.urls import reverse

from core.models import Token
from django.conf import settings


@pytest.fixture
def data_param():
    return [
        "date",
        "name",
        "rooms",
        "slots",
        "timeline"
    ]


@pytest.fixture
def slots_param():
    return [
        "event_id",
        "event_type",
        "title",
        "speakers",
        "begin_time",
        "end_time",
        "is_remote",
        "recording_policy",
        "language",
        "python_level",
        "break_event"
    ]


def test_list_schedule(data_param, slots_param, bare_user, drf_api_client):
    url = reverse("events:schedule-list")
    token = Token.objects.get_or_create(user=bare_user)
    drf_api_client.credentials(HTTP_AUTHORIZATION=str(token[0]))
    response = drf_api_client.get(url)

    for event in response.json()['data']:
        assert list(event.keys()) == data_param
        assert event['date'] in settings.EVENTS_DAY_NAMES.keys()
        assert event['name'] in settings.EVENTS_DAY_NAMES.values()
        for room in event['rooms']:
            for schedule_event in event['slots'][room]:
                assert list(schedule_event.keys()) == slots_param

    assert response.status_code == 200
