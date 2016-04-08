import datetime

from django.db import models
from django.db.models import Q
from django.utils.formats import time_format
from django.utils.translation import ugettext_lazy as _

from core.models import BigForeignKey, make_choices_enum
from core.utils import time_add


EventDay = make_choices_enum('EventDay', [
    ('1', datetime.date(2016, 6, 3), _('Day 1')),
    ('2', datetime.date(2016, 6, 4), _('Day 2')),
    ('3', datetime.date(2016, 6, 5), _('Day 3')),
])


class Location(models.Model):

    slug = models.SlugField(
        primary_key=True,
        verbose_name=_('slug'),
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_('name'),
    )

    class Meta:
        ordering = ['pk']
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    def __str__(self):
        return self.name


class StartTime(models.Model):

    time = models.TimeField(
        primary_key=True,
        verbose_name=_('time'),
    )

    class Meta:
        ordering = ['time']
        verbose_name = _('start time')
        verbose_name_plural = _('start times')

    def __str__(self):
        return time_format(self.time)


class ConferenceEvent(models.Model):

    day = models.DateField(
        choices=EventDay.choices,
        db_index=True,
        verbose_name=_('day'),
    )
    start_time = models.ForeignKey(
        to=StartTime,
        verbose_name=_('start time'),
    )

    class Meta:
        abstract = True


class TalkQuerySet(models.QuerySet):
    def filter_overlapping(self, day, location, timerange, exclude=None):
        """Filter talks that overlaps the given time range.

        If a talk overlaps the time range, its start time will be between
        `timerange.start` and `timerange.start - talk.duration`. Theoratically,
        we can do a calculation with column refs, something like::

            SELECT * FROM talks WHERE ... AND
            talks.start_time_id - talks.duration >= timerange.start

        but I didn't find a good way to express this with Django's `F()`
        expression. Fortunately we only have two kinds of talk durations, and
        a simple OR solves the problem. :p

        See also: `core.utils.TimeRange.overlaps`.
        """
        start_25 = time_add(
            day, timerange.start, datetime.timedelta(minutes=-25),
        )
        start_45 = time_add(
            day, timerange.start, datetime.timedelta(minutes=-45),
        )
        qs = (
            self
            .filter(
                day=day, location=location,
                start_time__time__lt=timerange.end,
            )
            .filter(
                Q(duration=Talk.Duration['25'].value,
                  start_time__time__gte=start_25) |
                Q(duration=Talk.Duration['45'].value,
                  start_time__time__gte=start_45)
            )
        )
        if isinstance(exclude, self.model) and exclude.pk:
            qs = qs.exclude(pk=exclude.pk)
        return qs


class Talk(ConferenceEvent):

    proposal = BigForeignKey(
        to='proposals.TalkProposal',
        limit_choices_to={'accepted': True},
        verbose_name=_('proposal'),
    )

    Duration = make_choices_enum('Duration', [
        ('25', datetime.timedelta(minutes=25), _('25 minutes')),
        ('45', datetime.timedelta(minutes=45), _('45 minutes')),
    ])
    duration = models.DurationField(
        choices=Duration.choices,
        db_index=True,
        verbose_name=_('duration'),
    )

    location = models.ForeignKey(
        to=Location,
        verbose_name=_('location'),
    )

    objects = TalkQuerySet.as_manager()

    class Meta:
        ordering = ['day', 'start_time', 'location']
        verbose_name = _('talk')
        verbose_name_plural = _('talks')

    def __str__(self):
        return self.proposal.title


class EventQuerySet(models.QuerySet):
    def filter_overlapping(self, day, location, timerange, exclude):
        """Filter events that overlaps the given time range.

        This uses the same logic as `core.utils.TimeRange.overlaps`.
        """
        qs = self.filter(
            day=day,
            location_set__slug=location.slug,
            start_time__time__lt=timerange.end,
            end_time__gt=timerange.start,
        )
        if isinstance(exclude, self.model) and exclude.pk:
            qs = qs.exclude(pk=exclude.pk)
        return qs


class Event(ConferenceEvent):

    name = models.CharField(
        max_length=50,
        verbose_name=_('name'),
    )
    name_zh = models.CharField(
        max_length=25,
        blank=True,
        verbose_name=_('name (Chinese)'),
    )

    end_time = models.TimeField(
        db_index=True,
        verbose_name=_('end time'),
    )

    location_set = models.ManyToManyField(
        to=Location,
        verbose_name=_('locations'),
    )

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ['day', 'start_time', 'end_time']
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __str__(self):
        return self.name
