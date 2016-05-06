from django.contrib import admin

from .models import SponsoredEvent


@admin.register(SponsoredEvent)
class SponsoredEventAdmin(admin.ModelAdmin):
    fields = [
        'host', 'title', 'slug', 'category', 'language',
        'abstract', 'python_level', 'detailed_description',
        'recording_policy', 'slide_link',
    ]
    search_fields = ['title', 'abstract']
    list_display = ['title', 'category', 'language', 'python_level']
    list_filter = ['category', 'language', 'python_level']
    prepopulated_fields = {'slug': ['title']}
    raw_id_fields = ['host']
