import datetime
import functools
import json
import urllib.parse

import pytz

from django.conf import settings
from django.contrib.staticfiles import finders
from django.urls import reverse, reverse_lazy
from django.db import models
from django.utils.timezone import make_naive
from django.utils.translation import get_language, gettext, gettext_lazy as _

from core.models import (
    BigForeignKey, EventInfo,
    ConferenceRelated, DefaultConferenceManagerMixin,
)
from core.utils import format_html_lazy
from proposals.models import TalkProposal, TutorialProposal, PrimarySpeaker
from sponsors.models import Sponsor


MIDNIGHT_TIME = datetime.time(tzinfo=pytz.timezone('Asia/Taipei'))

EVENT_DATETIME_START_END = (
    datetime.datetime.combine(
        min(settings.EVENTS_DAY_NAMES.keys()),
        MIDNIGHT_TIME,
    ),
    datetime.datetime.combine(
        max(settings.EVENTS_DAY_NAMES.keys()) + datetime.timedelta(days=1),
        MIDNIGHT_TIME,
    ),
)


class TimeManager(models.Manager):
    def get(self, value):
        """We only has one field, so let's make it available without keyword.
        """
        return super().get(value=value)


class LimitedTimeManager(TimeManager):
    def get_queryset(self):
        """Limit times to those in the current conference's time.
        """
        qs = super().get_queryset()
        return qs.filter(value__range=EVENT_DATETIME_START_END)


@functools.total_ordering
class Time(models.Model):

    value = models.DateTimeField(
        primary_key=True,
        verbose_name=_('value'),
    )

    objects = LimitedTimeManager()
    all_objects = TimeManager()

    class Meta:
        verbose_name = _('time')
        verbose_name_plural = _('times')
        ordering = ['value']

    def __str__(self):
        return str(make_naive(self.value))

    def __lt__(self, other):
        if not isinstance(other, Time):
            return NotImplemented
        if (not isinstance(self.value, datetime.datetime) or
                not isinstance(other.value, datetime.datetime)):
            return NotImplemented
        return self.value < other.value


class Location:
    """All possible location combinations.

    The numbering prefix helps to order events by locations. We need this
    information when resolving events in the same time period.

    Rules:

    1. The R3 events are put first.
    2. Belt and partial belt events are next, in that order.
    3. Block events in R0-2 are next, in that order.
    """
    R3    = '1-r3'
    ALL   = '2-all'
    R012  = '3-r012'
    R0    = '4-r0'
    R1    = '5-r1'
    R2    = '6-r2'
    R4    = '7-r4'
    OTHER = '8-oth'

    @classmethod
    def get_md_width(cls, value):
        return {
            '2-all': 4,
            '3-r012': 3,
            '4-r0': 1,
            '5-r1': 1,
            '6-r2': 1,
            '1-r3': 1,
            '7-r4': 1,
            '8-oth': 1,
        }[value]


EVENT_ROOMS = {Location.R0, Location.R1, Location.R2, Location.R3, Location.R4}


class BaseEvent(ConferenceRelated):
    """Base interface for all events in the schedule.
    """
    LOCATION_CHOICES = [
        (Location.ALL,   _('All rooms')),
        (Location.R012,  _('R1, R2, R3')),
        (Location.R0,    _('R1')),
        (Location.R1,    _('R2')),
        (Location.R2,    _('R3')),
        (Location.R3,    _('Multifunction room')),
        (Location.R4,    _('Goodideas Studio')),
        (Location.OTHER, _('Other')),
    ]
    location = models.CharField(
        max_length=6,
        choices=LOCATION_CHOICES,
        blank=True,
        null=True,
        db_index=True,
        verbose_name=_('location'),
    )

    begin_time = models.ForeignKey(
        to=Time,
        blank=True,
        null=True,
        related_name='begined_%(class)s_set',
        verbose_name=_('begin time'),
        on_delete=models.CASCADE,
    )

    end_time = models.ForeignKey(
        to=Time,
        blank=True,
        null=True,
        related_name='ended_%(class)s_set',
        verbose_name=_('end time'),
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class CustomEvent(BaseEvent):

    title = models.CharField(
        verbose_name=_('title'),
        max_length=140,
    )
    break_event = models.BooleanField(
        verbose_name=_('is break event'),
        default=False,
        help_text=_(
            "Whether this event is displays as a break. A break can be "
            "visually distinguished from \"real\" conference sessions, such "
            "as keynotes, talks, etc.",
        )
    )
    description = models.TextField(
        verbose_name=_('event description'), blank=True,
    )
    link_path = models.CharField(
        verbose_name=_('link path'),
        max_length=255, blank=True,
    )

    class Meta:
        verbose_name = _('custom event')
        verbose_name_plural = _('custom events')

    def __str__(self):
        return self.title


class KeynoteEvent(BaseEvent):

    speaker_name = models.CharField(
        verbose_name=_('speaker name'),
        max_length=100,
    )
    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=format_html_lazy(
            _("This is used to link to the speaker's introduction on the "
              "Keynote page, e.g. 'liang2' will link to "
              "'{link}#keynote-speaker-liang2'."),
            link=reverse_lazy('page', kwargs={'path': 'conference/keynotes'}),
        )
    )
    is_remote = models.BooleanField(
        verbose_name=_('is remote'),
        default=False,
    )

    class Meta:
        verbose_name = _('keynote event')
        verbose_name_plural = _('keynote events')

    def __str__(self):
        return gettext('Keynote: {speaker}'.format(
            speaker=self.speaker_name,
        ))

    def get_absolute_url(self):
        url = reverse('page', kwargs={'path': 'conference/keynotes'})
        split = urllib.parse.urlsplit(url)
        frag = 'keynote-speaker-{slug}'.format(slug=self.slug)
        return urllib.parse.urlunsplit(split._replace(fragment=frag))

    def get_static_data(self):
        path = '/'.join([
            settings.CONFERENCE_DEFAULT_SLUG,
            'assets/keynotes',
            f'{self.slug}.json',
        ])

        keynote_info = finders.find(path)
        if not keynote_info:
            raise FileNotFoundError(path)

        with open(keynote_info) as f:
            data = json.load(f)
        return data

    def get_static_data_for_locale(self, code=None):
        if code is None:
            code = get_language()
        code = code.split('-', 1)[0]

        data = self.get_static_data()
        data = {k: v[code] if isinstance(v, dict) and code in v else v for k, v in data.items()}
        return data


class JobListingsEvent(BaseEvent):

    sponsor = BigForeignKey(
        to=Sponsor,
        verbose_name=_("sponsor"),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Job Listings')
        verbose_name_plural = _('Job Listings')

    def __str__(self):
        return gettext('Open Role of Sponsor: {sponsor}'.format(
            sponsor=self.sponsor,
        ))


class SponsoredEvent(EventInfo, BaseEvent):

    host = BigForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_('host'),
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        allow_unicode=True,
        verbose_name=_('slug'),
    )

    class Meta:
        verbose_name = _('sponsored event')
        verbose_name_plural = _('sponsored events')

    def get_absolute_url(self):
        return reverse('events_sponsored_event_detail', kwargs={
            'slug': self.slug,
        })

    @property
    def speakers(self):
        yield PrimarySpeaker(user=self.host)


class ProposedEventManager(DefaultConferenceManagerMixin, models.Manager):

    proposal_attr = 'proposal'
    conference_attr = 'proposal__conference'

    def get_queryset(self):
        """We almost always need the proposal info, so let's always JOIN it.
        """
        return super().get_queryset().select_related(self.proposal_attr)


class ProposedTalkEvent(BaseEvent):

    proposal = BigForeignKey(
        to=TalkProposal,
        limit_choices_to={'accepted': True},
        verbose_name=_('proposal'),
        on_delete=models.CASCADE,
        unique=True,
    )
    is_remote = models.BooleanField(
        verbose_name=_('is remote'),
        default=False,
    )

    objects = ProposedEventManager()

    class Meta:
        verbose_name = _('talk event')
        verbose_name_plural = _('talk events')

    def __str__(self):
        return self.proposal.title

    def get_absolute_url(self):
        return reverse('events_talk_detail', kwargs={'pk': self.proposal.pk})


class ProposedTutorialEvent(BaseEvent):

    proposal = BigForeignKey(
        to=TutorialProposal,
        verbose_name=_('proposal'),
        on_delete=models.CASCADE,
        unique=True,
    )
    registration_link = models.URLField(
        verbose_name=_('registration link'),
        blank=True,
        default='',
    )

    objects = ProposedEventManager()

    class Meta:
        verbose_name = _('tutorial event')
        verbose_name_plural = _('tutorial events')

    def __str__(self):
        return self.proposal.title

    def get_absolute_url(self):
        return reverse('events_tutorial_detail', kwargs={
            'pk': self.proposal.pk,
        })


class Schedule(ConferenceRelated):

    html = models.TextField(
        verbose_name=_('HTML'),
    )
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')
        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self):
        return gettext('Schedule created at {}').format(self.created_at)
