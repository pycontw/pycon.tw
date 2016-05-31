import json

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):

    help = 'Load talk proposals from data dumped by `manage.py dumpdata`.'

    def add_arguments(self, parser):
        parser.add_argument('filename', help='Name of file to load data from')

    def handle(self, *args, filename, **options):
        with open(filename) as f:
            data = json.load(f)
        for dataset in data:
            model = apps.get_model(*dataset['model'].split('.'))
            fields = dataset.pop('fields', {})
            submitter = fields.pop('submitter', None)
            if submitter is not None:
                try:
                    submitter = User.objects.get(pk=submitter)
                except User.DoesNotExist:
                    submitter = User.objects.first()
            fields['submitter'] = submitter
            model.objects.update_or_create(fields, pk=dataset['pk'])
