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
        return self.data[obj.id]['stage_1']['+1']

    def dehydrate_stage_1_plus_0_count(self, obj):
        return self.data[obj.id]['stage_1']['+0']

    def dehydrate_stage_1_minus_0_count(self, obj):
        return self.data[obj.id]['stage_1']['-0']

    def dehydrate_stage_1_minus_1_count(self, obj):
        return self.data[obj.id]['stage_1']['-1']

    def dehydrate_stage_2_plus_1_count(self, obj):
        return self.data[obj.id]['stage_2']['+1']

    def dehydrate_stage_2_plus_0_count(self, obj):
        return self.data[obj.id]['stage_2']['+0']

    def dehydrate_stage_2_minus_0_count(self, obj):
        return self.data[obj.id]['stage_2']['-0']

    def dehydrate_stage_2_minus_1_count(self, obj):
        return self.data[obj.id]['stage_2']['-1']

    def prepare(self, obj):
        self.count = 0
        self.data[obj.id] = {
            'stage_1': {"+1": 0, "+0": 0, "-0": 0, "-1": 0},
            'stage_2': {"+1": 0, "+0": 0, "-0": 0, "-1": 0},
        }
        reviewer = []
        for review in obj.review_set.all().order_by('-updated'):
            if review.reviewer.email not in reviewer:
                reviewer.append(review.reviewer.email)
                self.data[obj.id]['stage_%d' % review.stage][review.vote] += 1
                self.count += 1

    def before_export(self, queryset, *args, **kwargs):
        self.data = {}
        super().before_export(queryset, *args, **kwargs)
        queryset = self.get_queryset()
        list(map(lambda obj: self.prepare(obj), queryset))

    class Meta:
        model = TalkProposal
        fields = [
            'id', 'title', 'category', 'python_level', 'duration', 'language',
            'name', 'email', 'cancelled', 'accepted', 'last_updated_at',
            'stage_1_plus_1_count', 'stage_1_plus_0_count',
            'stage_1_minus_0_count', 'stage_1_minus_1_count',
            'stage_2_plus_1_count', 'stage_2_plus_0_count',
            'stage_2_minus_0_count', 'stage_2_minus_1_count',
            'remoting_policy', 'first_time_speaker', 'referring_policy'
        ]
        export_order = fields
