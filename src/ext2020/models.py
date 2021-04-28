from django.db import models
from django.db.models import Q, F
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import StaticNode
from django.core.exceptions import ValidationError

from core.models import BigForeignKey
from proposals.models import TalkProposal
from events.models import SponsoredEvent, Time


# Create your models here.
class Attendee(models.Model):
    token = models.CharField(_('token'), max_length=64, unique=True)
    verified = models.BooleanField(_('verified'), default=False)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    verified_at = models.DateTimeField(_('verified at'), blank=True, null=True)

    class Meta:
        verbose_name = _('attendee')
        verbose_name_plural = _('attendees')

    def __str__(self):
        return self.token


class Venue(models.Model):
    name = models.CharField(verbose_name=_('Venue Name'), max_length=64)
    photo = models.CharField(verbose_name=_('Venue photo'), max_length=128, blank=True)

    address = models.CharField(_('Venue Address'), max_length=64, blank=True)
    community = models.CharField(_('Community'), max_length=64, blank=True)
    topic = models.CharField(_('Topic'), max_length=64, blank=True)

    capacity = models.IntegerField(_('Capacity Limit'), default=0)

    def get_choice_count(self):
        return self.choice_set.all().count()

    def get_soft_limit(self):
        return self.capacity * 0.8

    def get_photo_url(self):
        return StaticNode.handle_simple(self.photo)

    def get_events(self):
        # Get related events, whether the event is explicit set to the venue,
        # or with no venue set (lower priority)
        return CommunityTrackEvent.objects.filter(
            Q(venue=self) | Q(venue__isnull=True)
        ).order_by('begin_time__value', F('venue').desc(nulls_last=True)).distinct('begin_time__value')

    class Meta:
        verbose_name = _('community track venue')
        verbose_name_plural = _('community track venues')
        ordering = ['topic']

    def __str__(self):
        return self.name


class Choice(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, null=True, blank=True)
    selected_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('community track choice')
        verbose_name_plural = _('community track choices')

    def __str__(self):
        return "%s %s" % (self.venue, self.attendee.token if self.attendee else '?')


class CommunityTrackEvent(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True, blank=True)
    talk = BigForeignKey(TalkProposal, on_delete=models.CASCADE, null=True, blank=True)
    sponsored_event = BigForeignKey(SponsoredEvent, on_delete=models.CASCADE, null=True, blank=True)
    custom_event = models.CharField(max_length=140, blank=True)
    order = models.IntegerField(default=0)

    begin_time = models.ForeignKey(
        to=Time,
        blank=True,
        null=True,
        related_name='beginning_%(class)s_set',
        verbose_name=_('begin time'),
        on_delete=models.CASCADE,
    )

    end_time = models.ForeignKey(
        to=Time,
        blank=True,
        null=True,
        related_name='ending_%(class)s_set',
        verbose_name=_('end time'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('community track event')
        verbose_name_plural = _('community track events')
        ordering = ['begin_time', 'order']

    def __str__(self):
        return "%d. %s" % (self.order, self.get_event())

    def clean(self):
        values = [self.talk, self.sponsored_event, self.custom_event]
        count = len(tuple(filter(None, values)))

        if count > 1:
            raise ValidationError(
                _('You can only put either proposed_talk_event, sponsored_event or custom_event at once.'))

        if count <= 0:
            raise ValidationError(_('You need to put proposed_talk_event sponsored_event, or custom_event.'))

    def get_event(self):
        return self.talk or self.sponsored_event or self.custom_event
