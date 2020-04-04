from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from registry.models import Entry
from registry.admin import EntryAdmin


class CurrentConferenceFilter(admin.filters.SimpleListFilter):
    title = 'Current Conference'
    parameter_name = 'current'

    def lookups(self, request, model_admin):
        return [
            (None, _('Current')),
            ('other', _('Other')),
            ('all', _('All')),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'all':
            return queryset
        elif self.value() == 'other':
            return queryset.exclude(key__startswith=f'{settings.CONFERENCE_DEFAULT_SLUG}')

        return queryset.filter(key__startswith=f'{settings.CONFERENCE_DEFAULT_SLUG}')

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }


class PyConEntryAdmin(EntryAdmin):
    list_filter = (CurrentConferenceFilter, ) + EntryAdmin.list_filter


admin.site.unregister(Entry)
admin.site.register(Entry, PyConEntryAdmin)
