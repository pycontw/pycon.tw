import pytest

from django.utils.timezone import make_naive

from events import renderers


@pytest.fixture
def simple_renderer(mocker):

    def _simple_block_renderer(
            event, time_map, events, extra_classes=None, *,
            min_height=0, max_height=None):
        if extra_classes:
            fmt = '|{event} ({classes})| '
        else:
            fmt = '|{event}| '
        return fmt.format(classes=' '.join(extra_classes or []), event=event)

    def _simple_attached_period_renderer(begin, end):
        return '|{0.hour}:{0:%M} {1.hour}:{1:%M}| '.format(
            make_naive(begin.value), make_naive(end.value),
        )

    def _simple_columned_period_renderer(times, events):
        html = '|{}| '.format(
            ' '.join(
                '{0.hour}:{0:%M}'.format(make_naive(time.value))
                for time in times
            )
        )
        return html, len(events)

    mocker.patch.multiple(
        'events.renderers',
        render_block=_simple_block_renderer,
        render_attached_period=_simple_attached_period_renderer,
        render_columned_period=_simple_columned_period_renderer,
    )


@pytest.mark.usefixtures('simple_renderer')
def test_render_belt_events_row(parser, utils, keynote_belt_event):
    times = [keynote_belt_event.begin_time, keynote_belt_event.end_time]
    rendered = renderers.render_row(times, [keynote_belt_event])
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        |9:00 10:00|
        <div class="time-table__slot">
          <div class="row">
            |9:00 10:00|
            |Keynote: Amber Brown|
          </div>
        </div>
    """)


@pytest.mark.usefixtures('simple_renderer')
def test_render_partial_belt_events_row(
        parser, utils,
        partial_belt_begin_time, partial_belt_end_time, partial_belt_events):
    times = [partial_belt_begin_time, partial_belt_end_time]
    rendered = renderers.render_row(times, partial_belt_events)
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        |1:00 2:00|
        <div class="time-table__slot">
          <div class="row">
            |1:00 2:00|
            |Refreshment|
          </div>
        </div>
    """)


@pytest.mark.usefixtures('simple_renderer')
def test_render_partial_belt_block_events_row(
        parser, utils, partial_belt_block_begin_time,
        partial_belt_block_end_time, partial_belt_block_events):
    times = [partial_belt_block_begin_time, partial_belt_block_end_time]
    rendered = renderers.render_row(times, partial_belt_block_events)
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        |3:00 4:00|
        <div class="time-table__slot">
          <div class="row">
            |3:00 4:00|
            |Refreshment|
            |Free-market sub-orbital tattoo|
          </div>
        </div>
    """)


@pytest.mark.usefixtures('simple_renderer')
def test_render_partial_block_events_row(
        parser, utils, partial_block_begin_time,
        partial_block_end_time, partial_block_events):
    times = [partial_block_begin_time, partial_block_end_time]
    rendered = renderers.render_row(times, partial_block_events)
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        |5:00 6:00|
        <div class="time-table__slot">
          <div class="row">
            |5:00 6:00|
            |Boost Maintainability|
            |We Made the PyCon TW 2016 Website|
            |Deep Learning and Application in Python|
          </div>
        </div>
    """)


@pytest.mark.usefixtures('simple_renderer')
def test_render_block_events_row(
        parser, utils, block_begin_time, block_end_time, block_events):
    times = [block_begin_time, block_end_time]
    rendered = renderers.render_row(times, block_events)
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        |7:00 8:00|
        <div class="time-table__slot">
          <div class="row">
            |7:00 8:00|
            |Boost Maintainability|
            |We Made the PyCon TW 2016 Website|
            |Deep Learning and Application in Python|
            |Free-market sub-orbital tattoo|
          </div>
        </div>
    """)


@pytest.mark.usefixtures('simple_renderer')
def test_render_mismatch_block_events_row(
        parser, utils, mismatch_block_begin_time, mismatch_block_mid_time,
        mismatch_block_end_time, mismatch_block_events):
    times = [
        mismatch_block_begin_time,
        mismatch_block_mid_time,
        mismatch_block_end_time,
    ]
    rendered = renderers.render_row(times, mismatch_block_events)
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        |9:00 10:00 11:00|
        <div class="time-table__slot">
          <div class="row">
            |9:00 11:00|
            |Refreshment|
            |9:00 10:00|
            |Free-market sub-orbital tattoo|
          </div>
        </div>
    """)


@pytest.mark.usefixtures('simple_renderer')
def test_render_multirow_block_events_row(
        parser, utils, multirow_block_begin_time, multirow_block_mid_time,
        multirow_block_end_time, multirow_block_events):
    times = [
        multirow_block_begin_time,
        multirow_block_mid_time,
        multirow_block_end_time,
    ]
    rendered = renderers.render_row(times, multirow_block_events)
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        |12:00 13:00 14:00|
        <div class="time-table__slot">
          <div class="row">
            |12:00 13:00|
            |Boost Maintainability|
            |We Made the PyCon TW 2016 Website|
            |Deep Learning and Application in Python|
            |12:00 14:00|
            |Free-market sub-orbital tattoo (pull-right)|
            |13:00 14:00|
            |Refreshment|
          </div>
        </div>
    """)
