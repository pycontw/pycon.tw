from django.contrib import admin
from django.db.models import Q
from django.utils.timezone import make_naive
from django.utils.translation import ugettext_lazy as _

from .models import (
    CustomEvent, KeynoteEvent, ProposedTalkEvent, SponsoredEvent,
    Time, Schedule, DAY_1, DAY_2, DAY_3,
)


class TimeRangeFilter(admin.SimpleListFilter):

    title = _('time value')
    parameter_name = 'time-range'

    def lookups(self, request, model_admin):
        return [
            ('day1', _('Day 1')),
            ('day2', _('Day 2')),
            ('day3', _('Day 3')),
        ]

    def queryset(self, request, queryset):
        try:
            query = {
                'day1': Q(value__date=DAY_1),
                'day2': Q(value__date=DAY_2),
                'day3': Q(value__date=DAY_3),
            }[self.value()]
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

    get_month.short_description = _('month')
    get_day.short_description = _('day')
    get_hour.short_description = _('hour')
    get_minute.short_description = _('minute')


class EventTimeRangeFilter(admin.SimpleListFilter):

    def lookups(self, request, model_admin):
        return [
            ('day1', _('Day 1')),
            ('day2', _('Day 2')),
            ('day3', _('Day 3')),
        ]

    def queryset(self, request, queryset):
        try:
            filter_kwargs = {
                'day1': {self.field_name + '__value__date': DAY_1},
                'day2': {self.field_name + '__value__date': DAY_2},
                'day3': {self.field_name + '__value__date': DAY_3},
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
    fields = ['conference', 'title', 'begin_time', 'end_time', 'location']
    search_fields = ['title']
    list_display = ['title', 'begin_time', 'end_time', 'location']
    list_filter = [BeginTimeRangeFilter, EndTimeRangeFilter, 'location']


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
