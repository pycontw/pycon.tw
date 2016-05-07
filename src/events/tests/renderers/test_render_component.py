import pytest

from proposals.models import AdditionalSpeaker

from events import renderers
from events.models import Location, Time, CustomEvent, ProposedTalkEvent


@pytest.fixture
def custom_partial_belt_event(db):
    e = CustomEvent.objects.create(
        title='Job Fair',
        begin_time=Time.objects.get('2016-06-04 14:45'),
        end_time=Time.objects.get('2016-06-04 15:15'),
        location=Location.ALL,
    )
    return e


@pytest.fixture
def proposed_talk_block_event(accepted_talk_proposal, another_user):
    e = ProposedTalkEvent.objects.create(
        proposal=accepted_talk_proposal,
        begin_time=Time.objects.get('2016-06-03 16:00'),
        end_time=Time.objects.get('2016-06-03 16:45'),
        location=Location.R0,
    )
    AdditionalSpeaker.objects.create(
        user=another_user, proposal=accepted_talk_proposal,
    )
    return e


def test_render_customevent(utils, custom_partial_belt_event):
    rendered = renderers.render_customevent(custom_partial_belt_event)
    assert utils.is_safe(rendered)
    assert rendered == '<div class="event-title">Job Fair</div>'


def test_render_keynoteevent(utils, keynote_belt_event):
    rendered = renderers.render_keynoteevent(keynote_belt_event)
    assert utils.is_safe(rendered)
    assert rendered == (
        '<div class="event-title">Keynote &mdash; '
        '<a href="/en-us/events/keynotes/#keynote-speaker-amber-brown">'
        'Amber Brown</a></div>'
    )


def test_render_proposedtalkevent(utils, proposed_talk_block_event):
    rendered = renderers.render_proposedtalkevent(proposed_talk_block_event)
    assert utils.is_safe(rendered)
    assert rendered == (
        '<a href="/en-us/events/talk/42/">'
        '<div class="event-title">Beyond the Style Guides&lt;br&gt;</div>'
        '<div class="event-speakers">User and Misaki Mei</div>'
        '<div class="event-language">ZHEN</div></a>'
    )


def test_render_sponsoredevent(utils, sponsored_block_event):
    rendered = renderers.render_sponsoredevent(sponsored_block_event)
    assert utils.is_safe(rendered)
    assert rendered == (
        '<a href="/en-us/events/talk/sponsored/camera-engine/">'
        '<div class="event-title">Camera engine office woman lights</div>'
        '<div class="event-speakers">User</div>'
        '<div class="event-language">ZHZH</div></a>'
    )


@pytest.fixture
def events(
        custom_partial_belt_event, keynote_belt_event,
        proposed_talk_block_event, sponsored_block_event):
    return {
        'custom_event': custom_partial_belt_event,
        'keynote_event': keynote_belt_event,
        'proposed_talk_event': proposed_talk_block_event,
        'sponsored_event': sponsored_block_event,
    }


@pytest.mark.parametrize('event_key,expected', [
    ('custom_event', '<div class="event-title">Job Fair</div>'),
    ('keynote_event',
     '<div class="event-title">Keynote &mdash; '
     '<a href="/en-us/events/keynotes/#keynote-speaker-amber-brown">'
     'Amber Brown</a></div>'),
    ('proposed_talk_event',
     '<a href="/en-us/events/talk/42/">'
     '<div class="event-title">Beyond the Style Guides&lt;br&gt;</div>'
     '<div class="event-speakers">User and Misaki Mei</div>'
     '<div class="event-language">ZHEN</div></a>'),
    ('sponsored_event',
     '<a href="/en-us/events/talk/sponsored/camera-engine/">'
     '<div class="event-title">Camera engine office woman lights</div>'
     '<div class="event-speakers">User</div>'
     '<div class="event-language">ZHZH</div></a>'),
])
def test_render_event(utils, events, event_key, expected):
    event = events[event_key]
    rendered = renderers.render_event(event)
    assert utils.is_safe(rendered)
    assert rendered == expected


def test_render_event_fail(user):
    with pytest.raises(ValueError) as ctx:
        renderers.render_event(user)
    assert str(ctx.value) == (
        "No suitable renderer for <User: user@user.me> "
        "of <class 'users.models.User'>"
    )


@pytest.mark.parametrize('event_key,begin,end', [
    ('custom_event', '14:45', '15:15'),
    ('keynote_event', '9:00', '10:00'),
    ('proposed_talk_event', '16:00', '16:45'),
    ('sponsored_event', '11:00', '11:25'),
])
def test_render_attached_period(utils, events, event_key, begin, end):
    e = events[event_key]
    rendered = renderers.render_attached_period(
        e.begin_time.value,
        e.end_time.value,
    )
    assert utils.is_safe(rendered)
    assert rendered == (
        '<div class="col-xs-12 visible-xs-block visible-sm-block time-block">'
        '{} &ndash; {}</div>'.format(begin, end)
    )
