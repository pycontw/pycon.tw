import json

from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from proposals.models import TalkProposal, TutorialProposal


PROPOSAL_TYPE_MAPPING = {
    'talk': TalkProposal, 'tutorial': TutorialProposal
}


class Command(BaseCommand):
    help = "Export both talk and tutorial proposal info as JSON"

    def handle(self, *args, **options):
        joint_proposals = {}
        for ptype, Proposal in PROPOSAL_TYPE_MAPPING.items():
            joint_proposals[ptype] = self.export_proposals(Proposal)

        json_str = json.dumps(joint_proposals, cls=DjangoJSONEncoder)
        self.stdout.write(json_str)

    def export_proposals(self, Proposal):
        proposals = Proposal.objects.filter(
            cancelled=False
        ).select_related(
            'submitter__email',
            'submitter__speaker_name'
        )
        proposals_val = list(proposals.values(
            'submitter__speaker_name',
            'submitter__email',
            'title',
            'language',
            'duration',
            'python_level',
            'category',
        ))
        return proposals_val
