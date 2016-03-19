from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = [
        'reviewer', 'stage', 'proposal', 'vote', 'comment',
        'note',
        # 'updated',
    ]
    list_display = [
        'proposal', 'vote', 'reviewer', 'stage',
    ]
    list_filter = [
        'vote', 'stage',
    ]
