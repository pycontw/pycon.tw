from django.contrib import admin

from proposals.models import TalkProposal, TutorialProposal


class ProposalAdmin(admin.ModelAdmin):

    readonly_fields = ['submitter']
    search_fields = ['title', 'abstract']

    def has_add_permission(self, request):
        # Disable proposal submission via admin. Always use the public form!
        return False


@admin.register(TalkProposal)
class TalkProposalAdmin(ProposalAdmin):
    list_display = [
        'title', 'category', 'duration', 'language', 'target_audience',
        'python_level',
    ]
    list_filter = [
        'category', 'duration', 'language', 'target_audience', 'python_level',
    ]


@admin.register(TutorialProposal)
class TutorialProposalAdmin(ProposalAdmin):
    list_display = [
        'title', 'category', 'language', 'target_audience', 'python_level',
    ]
    list_filter = [
        'category', 'language', 'target_audience', 'python_level',
    ]
