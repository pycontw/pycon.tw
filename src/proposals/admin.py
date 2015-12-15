from django.contrib import admin

from proposals.models import TalkProposal


@admin.register(TalkProposal)
class TalkProposalAdmin(admin.ModelAdmin):

    list_display = [
        'title', 'category', 'duration', 'language', 'target_audience',
        'python_level',
    ]
    list_filter = [
        'category', 'duration', 'language', 'target_audience', 'python_level',
    ]
    readonly_fields = ['submitter']
    search_fields = ['title', 'abstract']

    def has_add_permission(self, request):
        # Disable proposal submission via admin. Always use the public form!
        return False
