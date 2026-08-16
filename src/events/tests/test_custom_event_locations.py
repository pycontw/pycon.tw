import datetime

import pytest
from django.conf import settings
from django.utils import timezone

from events.forms import CUSTOM_LOCATION, CustomEventForm
from events.models import CustomEvent, Location, Time


def make_time(date, hour):
    value = timezone.make_aware(datetime.datetime.combine(date, datetime.time(hour)))
    return Time.all_objects.create(value=value)


@pytest.mark.django_db
def test_custom_event_form_saves_predefined_location():
    form = CustomEventForm(data={
        'conference': settings.CONFERENCE_DEFAULT_SLUG,
        'title': 'Scheduled event',
        'location_mode': Location.R0,
        'description': '',
        'link_path': '',
    })

    assert form.is_valid(), form.errors
    event = form.save()
    assert event.location == Location.R0


@pytest.mark.django_db
def test_custom_event_form_saves_custom_location():
    form = CustomEventForm(data={
        'conference': settings.CONFERENCE_DEFAULT_SLUG,
        'title': 'Off-site event',
        'location_mode': CUSTOM_LOCATION,
        'custom_location': 'lobby',
        'description': '',
        'link_path': '',
    })

    assert form.is_valid(), form.errors
    event = form.save()
    assert event.location == 'lobby'


def test_custom_event_form_initializes_custom_location():
    form = CustomEventForm(instance=CustomEvent(location='lobby'))

    assert form.fields['location_mode'].initial == CUSTOM_LOCATION
    assert form.fields['custom_location'].initial == 'lobby'


def test_custom_event_form_requires_custom_location():
    form = CustomEventForm(data={
        'conference': settings.CONFERENCE_DEFAULT_SLUG,
        'title': 'Off-site event',
        'location_mode': CUSTOM_LOCATION,
        'custom_location': '',
        'description': '',
        'link_path': '',
    })

    assert not form.is_valid()
    assert form.errors['custom_location'] == ['Enter a custom location.']


def test_custom_event_form_limits_custom_location_to_twelve_characters():
    form = CustomEventForm(data={
        'conference': settings.CONFERENCE_DEFAULT_SLUG,
        'title': 'Off-site event',
        'location_mode': CUSTOM_LOCATION,
        'custom_location': 'x' * 13,
        'description': '',
        'link_path': '',
    })

    assert not form.is_valid()
    assert 'custom_location' in form.errors


@pytest.mark.django_db
def test_schedule_api_treats_custom_location_as_one_room(api_client):
    dates = list(settings.EVENTS_DAY_NAMES)
    for index, date in enumerate(dates):
        CustomEvent.objects.create(
            title=f'Event {index}',
            begin_time=make_time(date, 9),
            end_time=make_time(date, 10),
            location='lobby' if index == 0 else Location.R2,
        )

    response = api_client.get('/api/events/schedule/')

    assert response.status_code == 200
    first_day = response.json()['data'][0]
    assert 'lobby' in first_day['rooms']
    assert len(first_day['slots']['lobby']) == 1


@pytest.mark.django_db
def test_ccip_treats_custom_location_as_one_room(client):
    date = next(iter(settings.EVENTS_DAY_NAMES))
    event = CustomEvent.objects.create(
        title='Off-site event',
        begin_time=make_time(date, 9),
        end_time=make_time(date, 10),
        location='lobby',
    )

    response = client.get('/ccip/')

    assert response.status_code == 200
    data = response.json()
    session = next(item for item in data['sessions'] if item['id'] == f'event-{event.pk}')
    assert session['room'] == 'lobby'
    assert session['broadcast'] == []
    assert 'lobby' in {room['id'] for room in data['rooms']}
