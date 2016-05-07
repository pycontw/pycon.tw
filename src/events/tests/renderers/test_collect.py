import itertools

import sortedcontainers
import pytest

from events import renderers
from events.renderers import make_group


@pytest.fixture
def events(
        belt_event, partial_belt_events, partial_belt_block_events,
        partial_block_events, block_events, mismatch_block_events,
        multirow_block_events):
    return itertools.chain(
        [belt_event], partial_belt_events, partial_belt_block_events,
        partial_block_events, block_events, mismatch_block_events,
        multirow_block_events,
    )


def test_collect_event_groups(
        belt_event, partial_belt_events, partial_belt_block_events,
        partial_block_events, block_events, mismatch_block_events,
        multirow_block_events, make_time, events):
    groups = renderers.collect_event_groups(events)
    assert groups == sortedcontainers.SortedDict({
        (make_time(1), make_time(2)): make_group(*partial_belt_events),
        (make_time(3), make_time(4)): make_group(*partial_belt_block_events),
        (make_time(5), make_time(6)): make_group(*partial_block_events),
        (make_time(7), make_time(8)): make_group(*block_events),
        (make_time(9), make_time(10), make_time(11)): make_group(
            *mismatch_block_events),
        (make_time(12), make_time(13), make_time(14)): make_group(
            *multirow_block_events),
        (make_time(15), make_time(16)): make_group(belt_event),
    })
