from django.contrib import admin

from import_export.admin import ImportExportMixin

from .models import Review
from .resources import ReviewResource


@admin.register(Review)
class ReviewAdmin(ImportExportMixin, admin.ModelAdmin):
    fields = [
        'reviewer', 'stage', 'proposal', 'vote', 'comment', 'note',
        'discloses_comment', 'appropriateness', 'updated',
    ]
    readonly_fields = ['updated']
    list_display = [
        'proposal', 'vote', 'reviewer',
        'stage', 'discloses_comment', 'appropriateness',
    ]
    list_filter = [
        'vote', 'stage', 'discloses_comment', 'appropriateness',
    ]
    resource_class = ReviewResource
