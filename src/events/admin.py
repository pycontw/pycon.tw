from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.db.models import Q
from django.utils.html import format_html
from django.utils.timezone import make_naive
from django.utils.translation import (
    ugettext, gettext_lazy as _, pgettext_lazy as p,
)

from .forms import CustomEventForm
from .models import (
    CustomEvent, KeynoteEvent, ProposedTalkEvent, ProposedTutorialEvent,
    SponsoredEvent, Time, Schedule,
)


class TimeRangeFilter(admin.SimpleListFilter):

    title = _('time value')
    parameter_name = 'time-range'
    day_queries = {
        'day{}'.format(i): Q(value__date=date)
        for i, date in enumerate(settings.EVENTS_DAY_NAMES, 1)
    }

    def lookups(self, request, model_admin):
        return [
            ('day{}'.format(i), name)
            for i, name in enumerate(settings.EVENTS_DAY_NAMES.values(), 1)
        ]

    def queryset(self, request, queryset):
        try:
            query = self.day_queries[self.value()]
        except KeyError:
            return queryset
        return queryset.filter(query)


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):

    list_display = [
        '__str__', 'get_month', 'get_day', 'get_hour', 'get_minute',
    ]
    list_filter = [TimeRangeFilter]

    def get_month(self, instance):
        return make_naive(instance.value).strftime(r'%m')

    def get_day(self, instance):
        return make_naive(instance.value).strftime(r'%d')

    def get_hour(self, instance):
        return make_naive(instance.value).strftime(r'%H')

    def get_minute(self, instance):
        return make_naive(instance.value).strftime(r'%M')

    get_month.short_description = p('datetime component', 'month')
    get_day.short_description = p('datetime component', 'day')
    get_hour.short_description = p('datetime component', 'hour')
    get_minute.short_description = p('datetime component', 'minute')


class EventTimeRangeFilter(admin.SimpleListFilter):

    filter_kwargs_dict = {
        'day{}'.format(i): day
        for i, day in enumerate(settings.EVENTS_DAY_NAMES, 1)
    }

    def lookups(self, request, model_admin):
        return [
            ('day{}'.format(i), name)
            for i, name in enumerate(settings.EVENTS_DAY_NAMES.values(), 1)
        ]

    def queryset(self, request, queryset):
        try:
            filter_kwargs = {
                key: {self.field_name + '__value__date': value}
                for key, value in self.filter_kwargs_dict.items()
            }[self.value()]
        except KeyError:
            return queryset
        return queryset.filter(**filter_kwargs)


class BeginTimeRangeFilter(EventTimeRangeFilter):
    title = _('begin time')
    parameter_name = 'begin-time'
    field_name = 'begin_time'


class EndTimeRangeFilter(EventTimeRangeFilter):
    title = _('end time')
    parameter_name = 'end-time'
    field_name = 'end_time'


@admin.register(CustomEvent)
class CustomEventAdmin(admin.ModelAdmin):

    form = CustomEventForm
    search_fields = ['title']
    list_display = [
        'title', 'begin_time', 'end_time', 'location', 'break_event',
        'get_edit_link',
    ]
    list_filter = [
        BeginTimeRangeFilter, EndTimeRangeFilter, 'location', 'break_event',
    ]

    def get_edit_link(self, instance):
        return format_html(
            '<a href="{url}">{title}</a>',
            url=reverse('admin:events_customevent_change', args=[instance.pk]),
            title=ugettext('Edit'),
        )

    get_edit_link.short_description = ''


@admin.register(KeynoteEvent)
class KeynoteEventAdmin(admin.ModelAdmin):
    fields = [
        'conference', 'speaker_name', 'slug',
        'begin_time', 'end_time', 'location',
    ]
    search_fields = ['speaker_name']
    list_display = ['speaker_name', 'begin_time', 'end_time', 'location']
    list_filter = [BeginTimeRangeFilter, EndTimeRangeFilter, 'location']


@admin.register(ProposedTalkEvent)
class ProposedTalkEventAdmin(admin.ModelAdmin):
    fields = ['conference', 'proposal', 'begin_time', 'end_time', 'location']
    list_display = ['proposal', 'begin_time', 'end_time', 'location']
    list_filter = [BeginTimeRangeFilter, EndTimeRangeFilter, 'location']
    raw_id_fields = ['proposal']


@admin.register(ProposedTutorialEvent)
class ProposedTutorialEventAdmin(admin.ModelAdmin):
    fields = ['conference', 'proposal', 'begin_time', 'end_time', 'location']
    list_display = ['proposal', 'begin_time', 'end_time', 'location']
    list_filter = [BeginTimeRangeFilter, EndTimeRangeFilter, 'location']
    raw_id_fields = ['proposal']


@admin.register(SponsoredEvent)
class SponsoredEventAdmin(admin.ModelAdmin):
    fields = [
        'conference', 'host', 'title', 'slug', 'category', 'language',
        'abstract', 'python_level', 'detailed_description',
        'recording_policy', 'slide_link',
        'begin_time', 'end_time', 'location',
    ]
    list_display = ['title', 'begin_time', 'end_time', 'location']
    list_filter = [
        BeginTimeRangeFilter, EndTimeRangeFilter, 'location',
        'category', 'language', 'python_level',
    ]
    search_fields = ['title', 'abstract']
    prepopulated_fields = {'slug': ['title']}
    raw_id_fields = ['host']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    fields = ['html', 'created_at']
    readonly_fields = ['created_at']
    list_display = ['created_at']
