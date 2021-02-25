from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import Sponsor, OpenRole


@admin.register(Sponsor)
class SponsorAdmin(TranslationAdmin):
    fields = [
        'name', 'level', 'website_url', 'intro',
        'logo_svg', 'logo_image',
    ]
    list_display = ['name', 'level']
    list_filter = ['level']


@admin.register(OpenRole)
class OpenRoleAdmin(TranslationAdmin):
    fields = [
        'sponsor',
        'name',
        'description',
        'url',
    ]
    list_display = [
        'sponsor',
        'name',
        'description',
        'url',
    ]
