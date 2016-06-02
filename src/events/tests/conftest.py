import pytest

from events.models import Location, SponsoredEvent, Schedule, Time


@pytest.fixture
def sponsored_block_event(user):
    e = SponsoredEvent.objects.create(
        id=918,
        title='Camera engine office woman lights',
        slug='camera-engine',
        host=user,
        language='ZHZH',
        begin_time=Time.objects.get('2016-06-04 11:00'),
        end_time=Time.objects.get('2016-06-04 11:25'),
        location=Location.R2,
    )
    return e


@pytest.fixture
def schedule(db):
    return Schedule.objects.create(html='mmm')
