from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Venue,Choice


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo')



@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    # list_display = ('name', 'photo')
    pass
