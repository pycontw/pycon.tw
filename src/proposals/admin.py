from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from import_export.admin import ExportMixin

from .models import AdditionalSpeaker, TalkProposal, TutorialProposal
from .resources import TalkProposalResource
from reviews.models import Review

class AdditionalSpeakerInline(GenericTabularInline):
    model = AdditionalSpeaker
    fields = ['user', 'status', 'cancelled']
    ct_field = 'proposal_type'
    ct_fk_field = 'proposal_id'
    extra = 0


class ProposalAdmin(admin.ModelAdmin):

    def stage_1_plus_1_count(self,obj):
        return obj.review_set.filter(stage=1,vote=Review.Vote.PLUS_ONE).count()

    def stage_1_plus_0_count(self,obj):
        return obj.review_set.filter(stage=1,vote=Review.Vote.PLUS_ZERO).count()

    def stage_1_minus_0_count(self,obj):
        return obj.review_set.filter(stage=1,vote=Review.Vote.MINUS_ZERO).count()

    def stage_1_minus_1_count(self,obj):
        return obj.review_set.filter(stage=1,vote=Review.Vote.MINUS_ONE).count()

    def stage_2_plus_1_count(self,obj):
        return obj.review_set.filter(stage=2,vote=Review.Vote.PLUS_ONE).count()

    def stage_2_plus_0_count(self,obj):
        return obj.review_set.filter(stage=2,vote=Review.Vote.PLUS_ZERO).count()

    def stage_2_minus_0_count(self,obj):
        return obj.review_set.filter(stage=2,vote=Review.Vote.MINUS_ZERO).count()

    def stage_2_minus_1_count(self,obj):
        return obj.review_set.filter(stage=2,vote=Review.Vote.MINUS_ONE).count()



    list_display = [
        'title', 'category', 'duration', 'language',
        'python_level', 'remoting_policy', 'cancelled','accepted',
        'stage_1_plus_1_count','stage_1_plus_0_count','stage_1_minus_0_count','stage_1_minus_1_count',
        'stage_2_plus_1_count','stage_2_plus_0_count','stage_2_minus_0_count','stage_2_minus_1_count'
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
