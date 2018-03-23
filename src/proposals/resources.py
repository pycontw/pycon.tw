from import_export import fields, resources

from .models import TalkProposal


class TalkProposalResource(resources.ModelResource):

    name = fields.Field(attribute='submitter__speaker_name')
    email = fields.Field(attribute='submitter__email')

    class Meta:
        model = TalkProposal
        fields = [
            'id', 'title', 'category', 'python_level', 'duration',
            'language', 'name', 'email',
        ]
        export_order = fields
