import itertools

import sortedcontainers

from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.utils.timezone import make_naive
from django.utils.translation import ugettext, ugettext_lazy as _

from core.utils import html_join
from proposals.utils import format_names

from events.models import (
    DAY_NAMES, Location,
    CustomEvent, KeynoteEvent, ProposedTalkEvent, SponsoredEvent,
)


def render_customevent(e):
    return format_html(
        '<div class="slot-item__content">'
        '<div class="slot-item__title">{title}</div>'
        '</div>',
        title=e.title,
    )


def render_keynoteevent(e):
    return format_html(
        '<div class="slot-item__content talk">'
        '<div class="slot-item__title">{title}</div>'
        '<a href="{link}" class="talk__speaker">{speaker}</a>'
        '</div>',
        title=ugettext('Keynote'),
        link=e.get_absolute_url(),
        speaker=e.speaker_name,
    )


LANG_DISPLAY_MAP = {
    'ENEN': 'EN',
    'ZHZH': 'ZH',
    'ZHEN': _('EN Slides'),
    'TAI':  'TAI',
}


def render_proposedtalkevent(e):
    proposal = e.proposal
    speaker_names = [info.user.speaker_name for info in proposal.speakers]
    return format_html(
        '<div class="slot-item__content talk">'
        '<a href="{link}" class="talk__title">{title}</a>'
        '<a href="{link}#speaker-content" class="talk__speaker">{speakers}</a>'
        '<div class="talk__lang">{lang}</div>'
        '</div>',
        link=e.get_absolute_url(),
        title=proposal.title,
        speakers=format_names(speaker_names),
        lang=LANG_DISPLAY_MAP[proposal.language],
    )


def render_sponsoredevent(e):
    return format_html(
        '<div class="slot-item__content sponsored talk">'
        '<a href="{link}" class="talk__title">{title}</a>'
        '<a href="{link}#speaker-content" class="talk__speaker">{speaker}</a>'
        '<div class="talk__lang">{lang}</div>'
        '</div>',
        link=e.get_absolute_url(),
        title=e.title,
        speaker=e.host.speaker_name,
        lang=LANG_DISPLAY_MAP[e.language],
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


def render_block_location(location):
    return format_html(
        '<div class="slot-item__label slot-item__label--{key}">'
        '{display}</div>',
        key=location.split('-', 1)[-1],
        display={
            Location.ALL: '',
            Location.R012: 'R0 R1 R2',
            Location.R0: 'R0',
            Location.R1: 'R1',
            Location.R2: 'R2',
            Location.R3: 'R3',
        }[location],
    )


def _has_tall_event(events):
    return any(
        isinstance(e, ProposedTalkEvent) or isinstance(e, SponsoredEvent)
        for e in events
    )


def render_block(event, time_map, events, extra_classes=None, max_height=None):
    location = event.location
    height = time_map[event.end_time] - time_map[event.begin_time]
    if max_height is not None:
        height = min(height, max_height)
    if height == 1 and not _has_tall_event(events):
        height = 'small'
    return format_html(
        '<div class="slot-item slot-item--w{w} slot-item--h{h}{classes}">'
        '{location}{event}</div>',
        w=Location.get_md_width(location),
        h=height,
        location=render_block_location(location),
        event=render_event(event),
        classes=(' ' + ' '.join(extra_classes) if extra_classes else ''),
    )


def render_attached_period(begin, end):
    begin = make_naive(begin.value)
    end = make_naive(end.value)
    return format_html(
        '<div class="attached time-table__time">'
        '{begin_h}:{begin_m} &ndash; {end_h}:{end_m}</div>',
        begin_h=begin.hour, begin_m=begin.strftime(r'%M'),
        end_h=end.hour, end_m=end.strftime(r'%M'),
    )


def _render_blocks(events, time_map):
    """Render a R0-3 belt, a R0-2 partial belt (plus optionally a R3 event),
    or an all-block (with or without R3) format.
    """
    if events[0].location == Location.R3:
        # If this contains R3, shuffle it to the back.
        r3_event, *events = events
        r3_block = render_block(r3_event, time_map, events)
    else:
        r3_event = None
        r3_block = ''

    # Render period block for R3.
    # We cheat a little here: Times in R0-2 are supposed to be identical;
    # only R3 can be different. We just compare the first event's times
    # and R3's. If they are identical, R3 does not need its own period block,
    # otherwise it does.
    r3_period = ''
    rx_begin, rx_end = events[0].begin_time, events[0].end_time
    if r3_event:
        r3_begin = r3_event.begin_time
        r3_end = r3_event.end_time
        if r3_begin != rx_begin or r3_end != rx_end:
            r3_period = render_attached_period(r3_begin, r3_end)

    return format_html(
        '{r012_period}{r012_blocks}{r3_period}{r3_block}',
        r012_period=render_attached_period(rx_begin, rx_end),
        r012_blocks=html_join(
            '',
            (render_block(e, time_map, events) for e in events),
        ),
        r3_period=r3_period,
        r3_block=r3_block,
    )


def _render_multirow_subrow(event_iter, time_map, events):
    # Render period block for this row, and the first event.
    e0 = next(event_iter)
    cells = [
        render_attached_period(e0.begin_time, e0.end_time),
        render_block(e0, time_map, events)
    ]
    cols = Location.get_md_width(e0.location)

    # Keep rendering until we fill a row.
    while cols < 3:
        try:
            e = next(event_iter)
        except StopIteration:
            break
        cells.append(render_block(e, time_map, events))
        cols += Location.get_md_width(e.location)
    return cells


def _render_multirow(events, time_map, max_height):
    """Render a complex format that contains a multi-row R3 event.
    """
    sp_event, *events = events
    # Sort events by time, and then location. This is done here because
    # we need to exclude the R3 event (by putting it first).
    events = sorted(events, key=lambda e: (e.begin_time.value, e.location))
    event_iter = iter(events)

    # Render R0-R2 events in the first time period.
    cells = _render_multirow_subrow(event_iter, time_map, events)

    # Render the multi-row R3 event.
    cells.extend([
        render_attached_period(sp_event.begin_time, sp_event.end_time),
        render_block(sp_event, time_map, events, ['pull-right'], max_height),
    ])

    # Render the rest of the events.
    try:
        while True:
            cells += _render_multirow_subrow(event_iter, time_map, events)
    except StopIteration:
        pass

    # Join the results.
    return html_join('', cells)


def render_columned_period(times, events):
    cell_args = [
        _get_column_period_args(begin, end)
        for begin, end in zip(times[:-1], times[1:])
        if any(e.end_time == end for e in events)
    ]
    cells = format_html_join(
        '',
        '<div class="time__cell">{}:{}<br>|<br>{}:{}</div>',
        iter(cell_args),
    )
    height = len(cell_args)
    if height == 1 and not _has_tall_event(events):
        height = 'small'
    html = format_html(
        '<div class="columned time-table__time time-table__time--row-span '
        'time-table__time--h{height}">{cells}</div>',
        height=height,
        cells=cells,
    )
    return html, height


def _get_column_period_args(begin_time, end_time):
    begin_naive = make_naive(begin_time.value)
    end_naive = make_naive(end_time.value)
    return (
        begin_naive.hour,
        begin_naive.strftime('%M'),
        end_naive.hour,
        end_naive.strftime('%M'),
    )


def render_row(times, events):
    events = sorted(events, key=lambda e: e.location)
    times = sorted(times)
    time_map = {t: i for i, t in enumerate(times)}

    period_block, max_height = render_columned_period(times, events)
    try:
        sp_event = events[0]
    except IndexError:  # No events in this time period.
        content = ''
    else:
        if (sp_event.location != Location.R3 or sp_event.end_time <= times[1]):
            # If there's no R3 event, or if R3 event is not multi-row.
            content = _render_blocks(events, time_map)
        else:
            # If there is a multi-row R3 event.
            content = _render_multirow(events, time_map, max_height)
    return format_html(
        '{period}'
        '<div class="time-table__slot"><div class="row">{content}</div></div>',
        period=period_block,
        content=content,
    )


# This is made global so that we can easily test for equality.
def group_key(e):
    return e.location


def make_group(*events):
    return sortedcontainers.SortedListWithKey(events, key=group_key)


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

    head = mark_safe("""
        <div class="time-table__header">
          <div class="time-table__time"></div>
          <div class="time-table__slot">
            <div class="row">
              <div class="slot-item header-cell header-cell--r0">R0</div>
              <div class="slot-item header-cell header-cell--r1">R1</div>
              <div class="slot-item header-cell header-cell--r2">R2</div>
              <div class="slot-item header-cell header-cell--r3">R3</div>
            </div>
          </div>
        </div>
    """)
    body = html_join('', (
        render_row(times, group) for times, group in groups.items()
    ))
    return format_html(
        '<div class="time-table clearfix">{head}{body}</div>',
        head=head, body=body,
    )


def render_day(day, display):
    events = list(itertools.chain.from_iterable(
        _filter_events(Cls, day)
        for Cls in EVENT_CLASSES
    ))
    if not events:
        return ''
    return format_html(
        '<h2 id="{slug}" class="time-table-header">{display}</h2>{table}',
        slug=day.strftime(r'%Y-%m-%d'),
        display=display, table=render_table(day),
    )


def render_all():
    return html_join('', (
        render_day(day, display)
        for day, display in DAY_NAMES.items()
    ))
