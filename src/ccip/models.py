from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

from django.templatetags.static import StaticNode


class Venue(models.Model):
    name = models.CharField(verbose_name=_('Venue Name'), max_length=64)
    photo = models.CharField(verbose_name=_('Venue photo'), max_length=32)

    def get_photo_url(self):
        return StaticNode.handle_simple(self.photo)

    def __str__(self):
        return self.name


class Choice(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    attendee_token = models.CharField(verbose_name=_('attendee_token'), max_length=64)
    selected_time = models.DateTimeField()

    def __str__(self):
        return "%s %s" % (self.venue, self.attendee_token)
