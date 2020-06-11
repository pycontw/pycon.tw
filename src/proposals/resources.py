from import_export import fields, resources

from .models import TalkProposal
from reviews.models import Review

class TalkProposalResource(resources.ModelResource):

    name = fields.Field(attribute='submitter__speaker_name')
    email = fields.Field(attribute='submitter__email')
    stage_1_plus_1_count = fields.Field()
    stage_1_plus_0_count = fields.Field()
    stage_1_minus_0_count = fields.Field()
    stage_1_minus_1_count = fields.Field()
    stage_2_plus_1_count = fields.Field()
    stage_2_plus_0_count = fields.Field()
    stage_2_minus_0_count = fields.Field()
    stage_2_minus_1_count = fields.Field()

    def dehydrate_stage_1_plus_1_count(self, obj):
        return obj.review_set.filter(stage=1,vote=Review.Vote.PLUS_ONE).count()

    def dehydrate_stage_1_plus_0_count(self, obj):
        return obj.review_set.filter(stage=1,vote=Review.Vote.PLUS_ZERO).count()

    def dehydrate_stage_1_minus_0_count(self, obj):
        return obj.review_set.filter(stage=1,vote=Review.Vote.MINUS_ZERO).count()

    def dehydrate_stage_1_minus_1_count(self, obj):
        return obj.review_set.filter(stage=1,vote=Review.Vote.MINUS_ONE).count()

    def dehydrate_stage_2_plus_1_count(self, obj):
        return obj.review_set.filter(stage=2,vote=Review.Vote.PLUS_ONE).count()

    def dehydrate_stage_2_plus_0_count(self, obj):
        return obj.review_set.filter(stage=2,vote=Review.Vote.PLUS_ZERO).count()

    def dehydrate_stage_2_minus_0_count(self, obj):
        return obj.review_set.filter(stage=2,vote=Review.Vote.MINUS_ZERO).count()

    def dehydrate_stage_2_minus_1_count(self, obj):
        return obj.review_set.filter(stage=2,vote=Review.Vote.MINUS_ONE).count()

    class Meta:
        model = TalkProposal
        fields = [
            'id', 'title', 'category', 'python_level', 'duration',
            'language', 'name', 'email','cancelled','accepted',
            'stage_1_plus_1_count', 'stage_1_plus_0_count', 'stage_1_minus_0_count', 'stage_1_minus_1_count',
            'stage_2_plus_1_count', 'stage_2_plus_0_count', 'stage_2_minus_0_count', 'stage_2_minus_1_count'
        ]
        export_order = fields
