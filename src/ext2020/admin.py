from django.contrib import admin

from import_export.admin import ImportMixin

from .models import Attendee,Venue,Choice
from .resources import AttendeeResource

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
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo')



@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    # list_display = ('name', 'photo')
    pass
