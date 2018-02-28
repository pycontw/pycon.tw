import pytest
import pytz

from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive

from events.models import Location, SponsoredEvent, Time


cst = pytz.timezone('Asia/Taipei')


@pytest.fixture
def get_time(day):

    def _get_time(s):
        dt = parse_datetime(s)
        if is_naive(dt):
            dt = cst.localize(dt)
        return Time.objects.get(dt)

    return _get_time


@pytest.fixture
def sponsored_block_event(user, get_time):
    e = SponsoredEvent.objects.create(
        id=918,
        title='Camera engine office woman lights',
        slug='camera-engine',
        host=user,
        language='ZHZH',
        begin_time=get_time('2016-06-04 11:00'),
        end_time=get_time('2016-06-04 11:25'),
        location=Location.R2,
    )
    return e


@pytest.fixture(autouse=True, scope='module')
def time_stub_manager(request):
    orig_objects, Time.objects = Time.objects, Time.all_objects

    def unstub_manager():
        Time.objects = orig_objects

    request.addfinalizer(unstub_manager)
