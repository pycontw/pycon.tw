import datetime
import json

import pytz

from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_time

from events.models import DAY_NAMES, Location, Time
from events.renderers import EVENT_CLASSES


cst = pytz.timezone('Asia/Taipei')

DAYS = list(DAY_NAMES.keys())


def _pop_time_kwargs(dataset):
    day, begin, end = dataset.pop('time')
    d = DAYS[day - 1]

    b_dt = datetime.datetime.combine(d, parse_time(begin))
    e_dt = datetime.datetime.combine(d, parse_time(end))
    return {
        'begin_time': Time.objects.get_or_create(value=cst.localize(b_dt))[0],
        'end_time': Time.objects.get_or_create(value=cst.localize(e_dt))[0],
    }


def _pop_location(dataset):
    location_name = dataset.pop('location').upper()
    return getattr(Location, location_name)


class Command(BaseCommand):

    help = 'Load events from data.'

    def add_arguments(self, parser):
        parser.add_argument('filename', help='Name of file to load data from')
        parser.add_argument(
            '--truncate',
            action='store_const',
            const=True,
            help='Truncate existing event data',
        )

    def handle(self, *args, filename, truncate=False, **options):
        if truncate:
            for Cls in EVENT_CLASSES:
                Cls.objects.all().delete()
        with open(filename) as f:
            data = json.load(f)
        for model_name, datasets in data.items():
            model = apps.get_model(*model_name.split('.'))
            for dataset in datasets:
                dataset['location'] = _pop_location(dataset)
                dataset.update(_pop_time_kwargs(dataset))
                model.objects.create(**dataset)
