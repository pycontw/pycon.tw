from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from import_export.admin import ImportMixin, ImportExportMixin

from .models import Attendee, Venue, Choice, CommunityTrackEvent
from .resources import AttendeeResource, VenueResource, CommunityTrackEventResource


# Register your models here.
@admin.register(Attendee)
class AttendeeAdmin(ImportMixin, admin.ModelAdmin):
    list_display = [
        'token', 'verified', 'created_at', 'verified_at'
    ]

    list_filter = [
        'verified',
    ]
    resource_class = AttendeeResource


@admin.register(Venue)
class VenueAdmin(ImportExportMixin, TranslationAdmin):
    list_display = ('name', 'photo', 'address', 'community', 'topic', 'capacity', )


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    # list_display = ('name', 'photo')
    pass


@admin.register(CommunityTrackEvent)
class CommunityTrackEvent(ImportExportMixin, admin.ModelAdmin):
    list_display = ('venue', 'talk', 'order', )
    list_filter = ('order', )

    resource_class = CommunityTrackEventResource
