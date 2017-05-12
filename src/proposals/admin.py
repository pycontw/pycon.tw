from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from import_export.admin import ExportMixin

from .models import AdditionalSpeaker, TalkProposal, TutorialProposal
from .resources import TalkProposalResource


class AdditionalSpeakerInline(GenericTabularInline):
    model = AdditionalSpeaker
    fields = ['user', 'status', 'cancelled']
    ct_field = 'proposal_type'
    ct_fk_field = 'proposal_id'
    extra = 0


class ProposalAdmin(admin.ModelAdmin):

    fields = [
        'conference', 'submitter', 'title', 'category', 'duration',
        'language', 'abstract', 'python_level', 'objective',
        'detailed_description', 'outline', 'supplementary',
        'recording_policy', 'slide_link', 'cancelled',
    ]
    search_fields = ['title', 'abstract']
    inlines = [AdditionalSpeakerInline]


@admin.register(TalkProposal)
class TalkProposalAdmin(ExportMixin, ProposalAdmin):
    fields = ProposalAdmin.fields + ['accepted']
    list_display = [
        'title', 'category', 'duration', 'language',
        'python_level', 'accepted',
    ]
    list_filter = [
        'category', 'duration', 'language', 'python_level', 'accepted',
    ]
    resource_class = TalkProposalResource


@admin.register(TutorialProposal)
class TutorialProposalAdmin(ProposalAdmin):
    list_display = ['title', 'category', 'language', 'python_level']
    list_filter = ['category', 'language', 'python_level']
