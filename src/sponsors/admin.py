from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import OpenRole, Sponsor


@admin.register(Sponsor)
class SponsorAdmin(TranslationAdmin):
    fields = [
        'name', 'level', 'website_url', 'intro', 'subtitle',
        'logo_svg', 'logo_image', 'order'
    ]
    list_display = ['name', 'level', 'order']
    list_filter = ['level']


@admin.register(OpenRole)
class OpenRoleAdmin(TranslationAdmin):
    fields = [
        'sponsor',
        'name',
        'description',
        'requirements',
        'url',
    ]
    list_display = [
        'sponsor',
        'name',
        'description',
        'url',
    ]
