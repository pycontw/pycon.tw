from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = [
        'reviewer', 'stage', 'proposal', 'score', 'comment',
        'note',
        # 'updated',
    ]
    list_display = [
        'proposal', 'score', 'reviewer', 'stage',
    ]
    list_filter = [
        'score', 'stage',
    ]
