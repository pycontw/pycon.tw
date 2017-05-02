from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import Sponsor


@admin.register(Sponsor)
class SponsorAdmin(TranslationAdmin):
    list_display = ['name', 'level']
    list_filter = ['level']
    fields = ['name', 'level', 'website_url', 'intro', 'logo']
