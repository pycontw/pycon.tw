from django.contrib import admin

from import_export.admin import ImportMixin

from .models import Attendee
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
