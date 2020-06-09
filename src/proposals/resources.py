from import_export import fields, resources

from .models import TalkProposal


class TalkProposalResource(resources.ModelResource):

    name = fields.Field(attribute='submitter__speaker_name')
    email = fields.Field(attribute='submitter__email')
    vote = fields.Field()

    def dehydrate_vote(self, obj):
        return sum([int(review.vote) for review in obj.review_set.all()])

    class Meta:
        model = TalkProposal
        fields = [
            'id', 'title', 'category', 'python_level', 'duration',
            'language', 'name', 'email','cancelled','accepted','vote'
        ]
        export_order = fields
