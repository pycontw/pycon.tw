import itertools

import sortedcontainers

from django.utils.html import format_html, format_html_join
from django.utils.timezone import make_naive
from django.utils.translation import ugettext

from core.utils import html_join
from proposals.utils import format_names

from events.models import (
    DAY_NAMES, Location,
    CustomEvent, KeynoteEvent, ProposedTalkEvent, SponsoredEvent,
)


def render_customevent(e):
    return format_html(
        '<div class="event-title">{title}</div>',
        title=e.title,
    )


def render_keynoteevent(e):
    return format_html(
        ugettext(
            '<div class="event-title">'
            'Keynote &mdash; <a href="{link}">{speaker}</a>'
            '</div>'
        ),
        link=e.get_absolute_url(),
        speaker=e.speaker_name,
    )


def render_proposedtalkevent(e):
    proposal = e.proposal
    speaker_names = [info.user.speaker_name for info in proposal.speakers]
    return format_html(
        '<a href="{link}">'
        '<div class="event-title">{title}</div>'
        '<div class="event-speakers">{speakers}</div>'
        '<div class="event-language">{lang}</div>'
        '</a>',
        link=e.get_absolute_url(),
        title=proposal.title,
        speakers=format_names(speaker_names),
        lang=proposal.language,
    )


def render_sponsoredevent(e):
    return format_html(
        '<a href="{link}">'
        '<div class="event-title">{title}</div>'
        '<div class="event-speakers">{speaker}</div>'
        '<div class="event-language">{lang}</div>'
        '</a>',
        link=e.get_absolute_url(),
        title=e.title,
        speaker=e.host.speaker_name,
        lang=e.language,
    )


def render_event(e):
    func_name = 'render_{cls}'.format(cls=type(e).__name__.lower())
    try:
        func = globals()[func_name]
    except KeyError:
        raise ValueError(
            'No suitable renderer for {!r} of {!r}'.format(e, type(e)),
        )
    return func(e)


def render_attached_period(begin, end):
    begin = make_naive(begin)
    end = make_naive(end)
    return format_html(
        '<div class="col-xs-12 visible-xs-block visible-sm-block time-block">'
        '{begin_h}:{begin_m} &ndash; {end_h}:{end_m}</div>',
        begin_h=begin.hour, begin_m=begin.strftime(r'%M'),
        end_h=end.hour, end_m=end.strftime(r'%M'),
    )


def _render_block(event, time_map, *extra_classes):
    return format_html(
        '<div class="col-xs-12 col-md-{w} event-v-{h} event-block{classes}">'
        '{event}</div>',
        w=(3 * Location.get_md_width(event.location)),
        h=time_map[event.end_time.value] - time_map[event.begin_time.value],
        event=render_event(event),
        classes=(' ' + ' '.join(extra_classes) if extra_classes else ''),
    )


def render_blocks(events, time_map):
    """Render a R0-3 belt, a R0-2 partial belt (plus optionally a R3 event),
    or an all-block (with or without R3) format.
    """
    if events[0].location == Location.R3:
        # If this contains R3, shuffle it to the back.
        r3_event, *events = events
        r3_block = _render_block(r3_event, time_map)
    else:
        r3_event = None
        r3_block = ''

    # Render period block for R3.
    # We cheat a little here: Times in R0-2 are supposed to be identical;
    # only R3 can be different. We just compare the first event's times
    # and R3's. If they are identical, R3 does not need its own period block,
    # otherwise it does.
    r3_period = ''
    rx_begin, rx_end = events[0].begin_time.value, events[0].end_time.value
    if r3_event:
        r3_begin = r3_event.begin_time.value
        r3_end = r3_event.end_time.value
        if r3_begin != rx_begin or r3_end != rx_end:
            r3_period = render_attached_period(r3_begin, r3_end)

    return format_html(
        '{r012_period}{r012_blocks}{r3_period}{r3_block}',
        r012_period=render_attached_period(rx_begin, rx_end),
        r012_blocks=html_join(
            '',
            (_render_block(e, time_map) for e in events),
        ),
        r3_period=r3_period,
        r3_block=r3_block,
    )


def _render_subrow(event_iter, time_map):
    # Render period block for this row, and the first event.
    e0 = next(event_iter)
    cells = [
        render_attached_period(e0.begin_time.value, e0.end_time.value),
        _render_block(e0, time_map)
    ]
    cols = Location.get_md_width(e0.location)

    # Keep rendering until we fill a row.
    while cols < 3:
        try:
            e = next(event_iter)
        except StopIteration:
            break
        cells.append(_render_block(e, time_map))
        cols += Location.get_md_width(e.location)
    return cells


def render_multirow(events, time_map):
    """Render a complex format that contains a multi-row R3 event.
    """
    sp_event, *events = events
    # Sort events by time, and then location. This is done here because
    # we need to exclude the R3 event (by putting it first).
    events = sorted(events, key=lambda e: (e.begin_time.value, e.location))
    event_iter = iter(events)

    # Render R0-R2 events in the first time period.
    cells = _render_subrow(event_iter, time_map)

    # Render the multi-row R3 event.
    cells.extend([
        render_attached_period(
            sp_event.begin_time.value,
            sp_event.end_time.value,
        ),
        _render_block(sp_event, time_map, 'pull-right'),
    ])

    # Render the rest of the events.
    try:
        while True:
            cells += _render_subrow(event_iter, time_map)
    except StopIteration:
        pass

    # Join the results.
    return html_join('', cells)


def render_columned_period(times):

    def _get_kwargs(begin_time, end_time):
        begin_naive = make_naive(begin_time.value)
        end_naive = make_naive(end_time.value)
        return {
            'begin_h': begin_naive.hour,
            'begin_m': begin_naive.strftime('%M'),
            'end_h': end_naive.hour,
            'end_m': end_naive.strftime('%M'),
        }

    return html_join('', (
        format_html(
            '<div class="row">'
            '<div class="col-xs-12 hidden-xs hidden-sm time-block">'
            '{begin_h}:{begin_m} &ndash; {end_h}:{end_m}</div></div>',
            **_get_kwargs(begin, end)
        )
        for begin, end in zip(times[:-1], times[1:])
    ))


def render_row(times, events):
    events = sorted(events, key=lambda e: e.location)
    times = sorted(times)
    time_map = {t.value: i for i, t in enumerate(times)}
    try:
        sp_event = events[0]
    except IndexError:  # No events in this time period.
        content = ''
    else:
        if (sp_event.location != Location.R3 or sp_event.end_time <= times[1]):
            # If there's no R3 event, or if R3 event is not multi-row.
            content = render_blocks(events, time_map)
        else:
            # If there is a multi-row R3 event.
            content = render_multirow(events, time_map)
    return format_html(
        '<div class="row">'
        '<div class="col-md-2 time-column">{period}</div>'
        '<div class="col-md-10 event-column">'
        '<div class="row">{content}</div></div></div>',
        period=render_columned_period(times),
        content=content,
    )


# This is made global so that we can easily test for equality.
def _group_key(e):
    return e.location


def make_group(*events):
    return sortedcontainers.SortedListWithKey(events, key=_group_key)


def collect_event_groups(events):
    # Map of (sorted-tuple-of-times): [list-of-events].
    # This automatically sorts the keys by ``begin_time``.
    groups = sortedcontainers.SortedDict()

    for e in events:

        e_begin_time = e.begin_time
        e_end_time = e.end_time

        # Short circuit: If there's an identical group, just join it.
        if (e_begin_time, e_end_time) in groups:
            groups[(e_begin_time, e_end_time)].add(e)
            continue

        # Look for a suitable group.
        for key in groups.keys():
            begin_time, *_, end_time = key
            if ((begin_time <= e_begin_time and end_time >= e_end_time) or
                    (e_begin_time <= begin_time and e_end_time >= end_time)):
                # Either key can contain event, or event can contain key.
                events = groups.pop(key)
                events.add(e)
                times = sorted(set(key) | {e_begin_time, e_end_time})
                groups[tuple(times)] = events
                break
        else:
            # No suitable group. Let's make a new one.
            # This automatically sorts the items by location.
            groups[(e_begin_time, e_end_time)] = make_group(e)

    return groups


EVENT_CLASSES = (CustomEvent, KeynoteEvent, ProposedTalkEvent, SponsoredEvent)


def _filter_events(Cls, day):
    return (
        Cls.objects
        .filter(begin_time__value__date=day, end_time__value__date=day)
        .select_related('begin_time', 'end_time')
    )


def render_table(day):
    events = itertools.chain.from_iterable(
        _filter_events(Cls, day)
        for Cls in EVENT_CLASSES
    )
    groups = collect_event_groups(events)
    return html_join('', (
        render_row(times, group) for times, group in groups.items()
    ))


def render_all():
    return format_html_join(
        '', '<h2>{}</h2>{}',
        ((display, render_table(day))
         for day, display in DAY_NAMES.items())
    )
