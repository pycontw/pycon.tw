from django.contrib import admin

from .models import Attendee

# Register your models here.
@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = [
        'token', 'verified', 'created_at', 'verified_at'
    ]

    list_filter = [
        'verified', 
    ]
