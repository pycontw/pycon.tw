from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
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
