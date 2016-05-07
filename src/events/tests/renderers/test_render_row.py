import pytest

from django.utils.timezone import make_naive

from events import renderers


def _simple_attached_period_renderer(begin, end):
    return '|{0.hour}:{0:%M}|{1.hour}:{1:%M}|'.format(
        make_naive(begin),
        make_naive(end),
    )


@pytest.fixture
def simple_renderer(mocker):
    mocker.patch.multiple(
        renderers,
        render_event=str,
        render_attached_period=_simple_attached_period_renderer,
    )


@pytest.mark.usefixtures('simple_renderer')
def test_render_belt_events_row(parser, utils, keynote_belt_event):
    times = [keynote_belt_event.begin_time, keynote_belt_event.end_time]
    rendered = renderers.render_row(times, [keynote_belt_event])
    assert utils.is_safe(rendered)
    assert parser.arrange(rendered) == parser.arrange("""
        <div class="row">
          <div class="col-md-2 time-column">
            <div class="row">
              <div class="col-xs-12 hidden-xs hidden-sm time-block">
                9:00 &ndash; 10:00
              </div>
            </div>
          </div>
          <div class="col-md-10 event-column">
            <div class="row">
              |9:00|10:00|
              <div class="col-xs-12 col-md-12 event-v-1 event-block">
                Keynote: Amber Brown
              </div>
            </div>
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
        <div class="row">
          <div class="col-md-2 time-column">
            <div class="row">
              <div class="col-xs-12 hidden-xs hidden-sm time-block">
                1:00 &ndash; 2:00
              </div>
            </div>
          </div>
          <div class="col-md-10 event-column">
            <div class="row">
              |1:00|2:00|
              <div class="col-xs-12 col-md-9 event-v-1 event-block">
                Refreshment
              </div>
            </div>
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
        <div class="row">
          <div class="col-md-2 time-column">
            <div class="row">
              <div class="col-xs-12 hidden-xs hidden-sm time-block">
                3:00 &ndash; 4:00
              </div>
            </div>
          </div>
          <div class="col-md-10 event-column">
            <div class="row">
              |3:00|4:00|
              <div class="col-xs-12 col-md-9 event-v-1 event-block">
                Refreshment
              </div>
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                Free-market sub-orbital tattoo
              </div>
            </div>
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
        <div class="row">
          <div class="col-md-2 time-column">
            <div class="row">
              <div class="col-xs-12 hidden-xs hidden-sm time-block">
                5:00 &ndash; 6:00
              </div>
            </div>
          </div>
          <div class="col-md-10 event-column">
            <div class="row">
              |5:00|6:00|
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                Boost Maintainability
              </div>
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                We Made the PyCon TW 2016 Website
              </div>
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                Deep Learning and Application in Python
              </div>
            </div>
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
        <div class="row">
          <div class="col-md-2 time-column">
            <div class="row">
              <div class="col-xs-12 hidden-xs hidden-sm time-block">
                7:00 &ndash; 8:00
              </div>
            </div>
          </div>
          <div class="col-md-10 event-column">
            <div class="row">
              |7:00|8:00|
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                Boost Maintainability
              </div>
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                We Made the PyCon TW 2016 Website
              </div>
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                Deep Learning and Application in Python
              </div>
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                Free-market sub-orbital tattoo
              </div>
            </div>
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
        <div class="row">
          <div class="col-md-2 time-column">
            <div class="row">
              <div class="col-xs-12 hidden-xs hidden-sm time-block">
                9:00 &ndash; 10:00
              </div>
            </div>
            <div class="row">
              <div class="col-xs-12 hidden-xs hidden-sm time-block">
                10:00 &ndash; 11:00
              </div>
            </div>
          </div>
          <div class="col-md-10 event-column">
            <div class="row">
              |9:00|11:00|
              <div class="col-xs-12 col-md-9 event-v-2 event-block">
                Refreshment
              </div>
              |9:00|10:00|
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                Free-market sub-orbital tattoo
              </div>
            </div>
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
        <div class="row">
          <div class="col-md-2 time-column">
            <div class="row">
              <div class="col-xs-12 hidden-xs hidden-sm time-block">
                12:00 &ndash; 13:00
              </div>
            </div>
            <div class="row">
              <div class="col-xs-12 hidden-xs hidden-sm time-block">
                13:00 &ndash; 14:00
              </div>
            </div>
          </div>
          <div class="col-md-10 event-column">
            <div class="row">
              |12:00|13:00|
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                Boost Maintainability
              </div>
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                We Made the PyCon TW 2016 Website
              </div>
              <div class="col-xs-12 col-md-3 event-v-1 event-block">
                Deep Learning and Application in Python
              </div>
              |12:00|14:00|
              <div class="col-xs-12 col-md-3 event-v-2 event-block pull-right">
                Free-market sub-orbital tattoo
              </div>
              |13:00|14:00|
              <div class="col-xs-12 col-md-9 event-v-1 event-block">
                Refreshment
              </div>
            </div>
          </div>
        </div>
    """)
