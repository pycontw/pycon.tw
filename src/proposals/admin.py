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
    list_display = [
        'title', 'category', 'duration', 'language',
        'python_level', 'remoting_policy', 'accepted',
    ]
    list_filter = [
        'cancelled', 'accepted',
        'category', 'duration', 'language', 'python_level',
    ]
    fields = [
        'conference', 'submitter', 'title', 'category', 'duration',
        'language', 'abstract', 'python_level', 'objective',
        'detailed_description', 'outline', 'supplementary',
        'recording_policy', 'slide_link', 'referring_policy', 'remoting_policy', 'cancelled',
        'accepted', 'slido_embed_link',
    ]
    raw_id_fields = ['submitter']
    search_fields = ['title', 'abstract']
    inlines = [AdditionalSpeakerInline]


@admin.register(TalkProposal)
class TalkProposalAdmin(ExportMixin, ProposalAdmin):
    resource_class = TalkProposalResource


@admin.register(TutorialProposal)
class TutorialProposalAdmin(ProposalAdmin):
    pass
