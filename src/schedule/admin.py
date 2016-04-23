from django.contrib import admin
from django.contrib.admin.widgets import AdminTimeWidget
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .forms import EventForm, TalkForm
from .models import Event, Location, StartTime, Talk


class MinuteOnlyTimeFieldMixin:
    formfield_overrides = {
        models.TimeField: {'widget': AdminTimeWidget(format='%H:%M')},
    }


def joined_locations(instance, sep=', '):
    return sep.join(str(location) for location in instance.location_set.all())

joined_locations.short_description = _('locations')


@admin.register(Event)
class EventAdmin(MinuteOnlyTimeFieldMixin, admin.ModelAdmin):
    list_display = ['name', 'day', 'start_time', 'end_time', joined_locations]
    form = EventForm


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(StartTime)
class StartTimeAdmin(admin.ModelAdmin):
    list_display = ['time']


@admin.register(Talk)
class TalkAdmin(MinuteOnlyTimeFieldMixin, admin.ModelAdmin):
    list_display = ['proposal', 'day', 'start_time', 'duration', 'location']
    form = TalkForm
