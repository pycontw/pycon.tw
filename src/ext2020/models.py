from django.db import models
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import StaticNode

from core.models import BigForeignKey
from proposals.models import TalkProposal
from events.models import SponsoredEvent


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
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    talk = BigForeignKey(TalkProposal, on_delete=models.CASCADE, null=True, blank=True)
    sponsored_event = BigForeignKey(SponsoredEvent, on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('community track event')
        verbose_name_plural = _('community track events')
        ordering = ['order']

    def __str__(self):
        return "%d. %s (%s)" % (self.order, self.get_event(), self.venue.name)

    def clean(self):
        if self.talk and self.sponsored_event:
            raise ValidationError(_('You can only put either proposed_talk_event or sponsored_event at once.'))

        if not self.talk and not self.sponsored_event:
            raise ValidationError(_('You need to put proposed_talk_event or sponsored_event.'))

    def get_event(self):
        return self.talk or self.sponsored_event
