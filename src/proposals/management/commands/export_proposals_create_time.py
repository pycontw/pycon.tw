import json
import pytz

from datetime import datetime
from django.utils import timezone
from proposals.models import TalkProposal, TutorialProposal
from django.core.management.base import BaseCommand

PROPOSAL_TYPE_MAPPING = {
    'talk': TalkProposal, 'tutorial': TutorialProposal
}

class Command(BaseCommand):
    help = "export proposal's create time(default UTC+8) as JSON"

    def handle(self, *args, **options):
        self.export_proposals_create_time()

    def export_proposals_create_time(self):
        joint_proposals = []
        for ptype, Proposal in PROPOSAL_TYPE_MAPPING.items():
            for p in Proposal.objects.all():
                timezone.activate(pytz.timezone('Asia/Taipei'))
                # ^you can edit 'Asia/Taipei to other area.'
                current_tz = timezone.get_current_timezone()
                time = p.created_at
                time = current_tz.normalize(time.astimezone(current_tz))
                time = datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
                joint_proposals.append({
                    'proposal_type(id)': ptype+'({})'.format(p.id),
                    'title': p.title,
                    'speaker_name': p.submitter.speaker_name,
                    'email': p.submitter.email,
                    'created_at': time
                })
        json_str = json.dumps(joint_proposals, sort_keys = False, indent=4, ensure_ascii=False)
        self.stdout.write(json_str)
    
