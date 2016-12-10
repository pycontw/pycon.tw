import pytest

from events import renderers
from events.models import Location, CustomEvent


@pytest.fixture
def simple_component_renderer(mocker):
    mocker.patch.multiple(
        'events.renderers',
        render_event=str,
        render_block_location=lambda v: '{} '.format(v),
    )


@pytest.fixture
def time_map(events):
    times = set()
    for e in events.values():
        times.add(e.begin_time)
        times.add(e.end_time)
    return {time: i for i, time in enumerate(sorted(times))}


# Hack to get all possible location values by introspection.
POSSIBLE_LOCATIONS = sorted(
    getattr(Location, k)
    for k in Location.__dict__ if k.isupper()
)


@pytest.mark.parametrize('location', POSSIBLE_LOCATIONS)
def test_render_block_location(parser, utils, location):
    rendered = renderers.render_block_location(location)
    assert utils.is_safe(rendered)

    expected = {
        Location.ALL: (
            '<div class="slot-item__label slot-item__label--all"></div>'
        ),
        Location.R012: (
            '<div class="slot-item__label slot-item__label--r012">'
            'R0 R1 R2</div>'
        ),
        Location.R0: (
            '<div class="slot-item__label slot-item__label--r0">'
            'R0</div>'
        ),
        Location.R1: (
            '<div class="slot-item__label slot-item__label--r1">'
            'R1</div>'
        ),
        Location.R2: (
            '<div class="slot-item__label slot-item__label--r2">'
            'R2</div>'
        ),
        Location.R3: (
            '<div class="slot-item__label slot-item__label--r3">'
            'R3</div>'
        ),
    }[location]
    assert parser.arrange(rendered) == parser.arrange(expected)


@pytest.mark.parametrize('event_key', [
    'custom_event', 'keynote_event', 'proposed_talk_event', 'sponsored_event',
])
@pytest.mark.usefixtures('simple_component_renderer')
def test_render_block(parser, utils, time_map, events, event_key):
    e = events[event_key]
    rendered = renderers.render_block(e, time_map, [e])
    assert utils.is_safe(rendered)

    expected = {
        'custom_event': """
            <div class="slot-item slot-item--w3 slot-item--hsmall">
              3-r012 Job Fair
            </div>""",
        'keynote_event': """
            <div class="slot-item slot-item--w4 slot-item--hsmall">
              2-all Keynote: Amber Brown
            </div>""",
        'proposed_talk_event': """
            <div class="slot-item slot-item--w1 slot-item--h1">
              4-r0 Beyond the Style Guides&lt;br&gt;
            </div>""",
        'sponsored_event': """
            <div class="slot-item slot-item--w1 slot-item--h1">
              6-r2 Camera engine office woman lights
            </div>""",
    }[event_key]
    assert parser.arrange(rendered) == parser.arrange(expected)


@pytest.mark.parametrize('event_key,begin,end', [
    ('custom_event', '14:45', '15:15'),
    ('keynote_event', '9:00', '10:00'),
    ('proposed_talk_event', '16:00', '16:45'),
    ('sponsored_event', '11:00', '11:25'),
])
def test_render_attached_period(utils, events, event_key, begin, end):
    e = events[event_key]
    rendered = renderers.render_attached_period(e.begin_time, e.end_time)
    assert utils.is_safe(rendered)
    assert rendered == (
        '<div class="attached time-table__time">{} &ndash; {}</div>'.format(
            begin, end,
        )
    )


@pytest.mark.parametrize('time_count', [2, 3, 4])
def test_render_columned_period(parser, utils, make_time, time_count):
    times = [make_time(h) for h in range(time_count)]
    rendered, _ = renderers.render_columned_period(times, [
        CustomEvent(
            title='M<3', location=Location.ALL,
            begin_time=begin_time, end_time=end_time,
        )
        for begin_time, end_time in zip(times[:-1], times[1:])
    ])
    assert utils.is_safe(rendered)

    expected = {
        2: (
            '<div class="columned time-table__time time-table__time--row-span '
            'time-table__time--hsmall">'
            '  <div class="time__cell">0:00<br>|<br>1:00</div>'
            '</div>'
        ),
        3: (
            '<div class="columned time-table__time time-table__time--row-span '
            'time-table__time--h2">'
            '  <div class="time__cell">0:00<br>|<br>1:00</div>'
            '  <div class="time__cell">1:00<br>|<br>2:00</div>'
            '</div>'
        ),
        4: (
            '<div class="columned time-table__time time-table__time--row-span '
            'time-table__time--h3">'
            '  <div class="time__cell">0:00<br>|<br>1:00</div>'
            '  <div class="time__cell">1:00<br>|<br>2:00</div>'
            '  <div class="time__cell">2:00<br>|<br>3:00</div>'
            '</div>'
        ),
    }[time_count]
    assert parser.arrange(rendered) == parser.arrange(expected)
