from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from import_export.admin import ExportMixin

from .models import AdditionalSpeaker, LLMReview, TalkProposal, TutorialProposal
from .resources import TalkProposalResource, TutorialProposalResource


class AdditionalSpeakerInline(GenericTabularInline):
    model = AdditionalSpeaker
    fields = ['user', 'status', 'cancelled']
    ct_field = 'proposal_type'
    ct_fk_field = 'proposal_id'
    extra = 0


class ProposalAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'duration',
        'language',
        'python_level',
        'accepted',
    ]
    list_filter = [
        'cancelled', 'accepted',
        'category', 'duration', 'language', 'python_level',
        'labels',
    ]
    raw_id_fields = ['submitter']
    search_fields = ['title', 'abstract']
    inlines = [AdditionalSpeakerInline]


class LLMReviewInline(admin.StackedInline):
    model = LLMReview
    fields = [
        'stage', 'summary', 'comment', 'translated_summary',
        'translated_comment', 'categories', 'vote', 'stage_diff',
        'translated_stage_diff', 'created_at',
    ]
    readonly_fields = ['created_at']
    can_delete = True
    max_num = 2
    min_num = 0
    extra = 1


@admin.register(TalkProposal)
class TalkProposalAdmin(ExportMixin, ProposalAdmin):
    resource_class = TalkProposalResource
    list_display = [
        'title',
        'category',
        'duration',
        'language',
        'python_level',
        'first_time_speaker',
        'accepted',
    ]
    inlines = [AdditionalSpeakerInline, LLMReviewInline]


@admin.register(TutorialProposal)
class TutorialProposalAdmin(ExportMixin, ProposalAdmin):
    resource_class = TutorialProposalResource
