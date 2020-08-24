from django.db import models
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import StaticNode

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
    photo = models.CharField(verbose_name=_('Venue photo'), max_length=128)

    def get_photo_url(self):
        return StaticNode.handle_simple(self.photo)

    def __str__(self):
        return self.name


class Choice(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    attendee_token = models.CharField(verbose_name=_('attendee_token'), max_length=64)
    selected_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.venue, self.attendee_token)
