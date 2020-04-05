import json
import pathlib

from django.conf import settings
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from registry.helper import reg

from proposals.models import TalkProposal
from reviews.models import TalkProposalSnapshot


PythonSerializer = serializers.get_serializer('python')


class Command(BaseCommand):

    help = 'Make snapshot for talk proposals.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--database',
            action='store_true',
            dest='from_db',
            help='Make snapshot from database.',
        )
        parser.add_argument(
            '--dump',
            metavar='FILE',
            dest='filename_str',
            help='Make snapshot from a data dump.',
        )

    def handle(self, *, from_db, filename_str, **options):
        if not (from_db ^ bool(filename_str)):
            raise CommandError(
                'Provide exactly one of --database of --dump FILE'
            )

        if filename_str:
            self.snapshot_from_dump(pathlib.Path(filename_str))
        else:
            self.snapshot_from_db()

    def snapshot_from_dump(self, file_path):
        with file_path.open() as f:
            dataset_list = json.load(f)
        self.make_snapshots(filter(
            lambda d: d['model'] == 'proposals.talkproposal',
            dataset_list,
        ))

    def snapshot_from_db(self):
        talk_proposal_qs = TalkProposal.objects.all()
        dataset_list = PythonSerializer().serialize(talk_proposal_qs)
        self.make_snapshots(dataset_list)

    @transaction.atomic
    def make_snapshots(self, dataset_iter):
        current_stage = reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.reviews.stage', 0)
        for dataset in dataset_iter:
            pk = dataset['pk']
            field_data = {
                k: v for k, v in dataset['fields'].items()
                if k != 'submitter'
            }
            dumped_json = json.dumps(field_data, cls=DjangoJSONEncoder)
            TalkProposalSnapshot.objects.update_or_create(
                proposal_id=pk, stage=current_stage,
                defaults={'dumped_json': dumped_json},
            )
