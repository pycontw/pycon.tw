import datetime

import pytest
import pytz

from events.models import Location, Time, CustomEvent, KeynoteEvent


cst = pytz.timezone('Asia/Taipei')


class RendererTestUtils:
    @staticmethod
    def is_safe(s):
        """Check whether a string is safe.

        This is Django's internal API, but we exploit it for easy testing.
        """
        return hasattr(s, '__html__')


@pytest.fixture
def utils():
    return RendererTestUtils


@pytest.fixture
def keynote_belt_event(db):
    e = KeynoteEvent.objects.get(speaker_name='Amber Brown')
    e.begin_time = Time.objects.get('2016-06-05 9:00')
    e.end_time = Time.objects.get('2016-06-05 10:00')
    e.location = Location.ALL
    e.save()
    return e


@pytest.fixture
def day():
    return datetime.date(2016, 8, 19)


@pytest.fixture
def make_time(day):

    def _make_time(h, m=0):
        dt = datetime.datetime.combine(day, datetime.time(h, m))
        return Time(value=cst.localize(dt))

    return _make_time


@pytest.fixture
def belt_begin_time(make_time):
    return make_time(15)


@pytest.fixture
def belt_end_time(make_time):
    return make_time(16)


@pytest.fixture
def belt_event(belt_begin_time, belt_end_time):
    return KeynoteEvent(
        speaker_name='Amber Brown',
        slug='amber-brown',
        begin_time=belt_begin_time,
        end_time=belt_end_time,
    )


@pytest.fixture
def partial_belt_begin_time(make_time):
    return make_time(1)


@pytest.fixture
def partial_belt_end_time(make_time):
    return make_time(2)


@pytest.fixture
def partial_belt_events(partial_belt_begin_time, partial_belt_end_time):
    event = CustomEvent(
        title='Refreshment',
        location=Location.R012,
        begin_time=partial_belt_begin_time,
        end_time=partial_belt_end_time,
    )
    return [event]


@pytest.fixture
def partial_belt_block_begin_time(make_time):
    return make_time(3)


@pytest.fixture
def partial_belt_block_end_time(make_time):
    return make_time(4)


@pytest.fixture
def partial_belt_block_events(
        partial_belt_block_begin_time, partial_belt_block_end_time):
    events = [
        CustomEvent(
            title='Refreshment',
            location=Location.R012,
            begin_time=partial_belt_block_begin_time,
            end_time=partial_belt_block_end_time,
        ),
        CustomEvent(
            title='Free-market sub-orbital tattoo',
            location=Location.R3,
            begin_time=partial_belt_block_begin_time,
            end_time=partial_belt_block_end_time,
        ),
    ]
    return events


@pytest.fixture
def partial_block_begin_time(make_time):
    return make_time(5)


@pytest.fixture
def partial_block_end_time(make_time):
    return make_time(6)


@pytest.fixture
def partial_block_events(partial_block_begin_time, partial_block_end_time):
    events = [
        CustomEvent(
            title='Boost Maintainability',
            location=Location.R0,
            begin_time=partial_block_begin_time,
            end_time=partial_block_end_time,
        ),
        CustomEvent(
            title='We Made the PyCon TW 2016 Website',
            location=Location.R1,
            begin_time=partial_block_begin_time,
            end_time=partial_block_end_time,
        ),
        CustomEvent(
            title='Deep Learning and Application in Python',
            location=Location.R2,
            begin_time=partial_block_begin_time,
            end_time=partial_block_end_time,
        ),
    ]
    return events


@pytest.fixture
def block_begin_time(make_time):
    return make_time(7)


@pytest.fixture
def block_end_time(make_time):
    return make_time(8)


@pytest.fixture
def block_events(block_begin_time, block_end_time):
    events = [
        CustomEvent(
            title='Boost Maintainability',
            location=Location.R0,
            begin_time=block_begin_time,
            end_time=block_end_time,
        ),
        CustomEvent(
            title='We Made the PyCon TW 2016 Website',
            location=Location.R1,
            begin_time=block_begin_time,
            end_time=block_end_time,
        ),
        CustomEvent(
            title='Deep Learning and Application in Python',
            location=Location.R2,
            begin_time=block_begin_time,
            end_time=block_end_time,
        ),
        CustomEvent(
            title='Free-market sub-orbital tattoo',
            location=Location.R3,
            begin_time=block_begin_time,
            end_time=block_end_time,
        ),
    ]
    return events


@pytest.fixture
def mismatch_block_begin_time(make_time):
    return make_time(9)


@pytest.fixture
def mismatch_block_mid_time(make_time):
    return make_time(10)


@pytest.fixture
def mismatch_block_end_time(make_time):
    return make_time(11)


@pytest.fixture
def mismatch_block_events(
        mismatch_block_begin_time, mismatch_block_mid_time,
        mismatch_block_end_time):
    events = [
        CustomEvent(
            title='Refreshment',
            location=Location.R012,
            begin_time=mismatch_block_begin_time,
            end_time=mismatch_block_end_time,
        ),
        CustomEvent(
            title='Free-market sub-orbital tattoo',
            location=Location.R3,
            begin_time=mismatch_block_begin_time,
            end_time=mismatch_block_mid_time,
        ),
    ]
    return events


@pytest.fixture
def multirow_block_begin_time(make_time):
    return make_time(12)


@pytest.fixture
def multirow_block_mid_time(make_time):
    return make_time(13)


@pytest.fixture
def multirow_block_end_time(make_time):
    return make_time(14)


@pytest.fixture
def multirow_block_events(
        multirow_block_begin_time, multirow_block_mid_time,
        multirow_block_end_time):
    events = [
        CustomEvent(
            title='Boost Maintainability',
            location=Location.R0,
            begin_time=multirow_block_begin_time,
            end_time=multirow_block_mid_time,
        ),
        CustomEvent(
            title='We Made the PyCon TW 2016 Website',
            location=Location.R1,
            begin_time=multirow_block_begin_time,
            end_time=multirow_block_mid_time,
        ),
        CustomEvent(
            title='Deep Learning and Application in Python',
            location=Location.R2,
            begin_time=multirow_block_begin_time,
            end_time=multirow_block_mid_time,
        ),
        CustomEvent(
            title='Free-market sub-orbital tattoo',
            location=Location.R3,
            begin_time=multirow_block_begin_time,
            end_time=multirow_block_end_time,
        ),
        CustomEvent(
            title='Refreshment',
            location=Location.R012,
            begin_time=multirow_block_mid_time,
            end_time=multirow_block_end_time,
        ),
    ]
    return events
