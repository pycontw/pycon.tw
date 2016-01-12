import logging
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils.timezone import now
from tabulate import tabulate
from proposals.models import TalkProposal, TutorialProposal

logger = logging.getLogger(__file__)

def str_stripper(s, max_len=32):
    if len(s) > max_len:
        return s[:max_len - len('...')] + '...'
    else:
        return s


class Command(BaseCommand):
    help = "Summarize the recent proposal submits."

    def add_arguments(self, parser):
        parser.add_argument(
            '--recent',
            metavar='N',
            type=int,
            default=3,
            help='Collect proposals submitted in the latest N days.'
        )

    def handle(self, *args, **options):
        recent_days = options['recent']
        if recent_days <= 0:
            raise CommandError(
                'Provide positive number of days, getting %d'
                % recent_days
            )
        self.stderr.write(
            'Collecting recent {:d} days proposals ...'
            .format(recent_days)
        )
        earliest_dt = now() - timedelta(days=recent_days)
        recent_lookup = Q(created_at__gte=earliest_dt) & Q(cancelled=False)
        recent_talks = TalkProposal.objects.filter(recent_lookup)
        recent_tutorials = TutorialProposal.objects.filter(recent_lookup)
        if not recent_talks.exists() and not recent_tutorials.exists():
            self.cry()
            return

        self.stdout.write(
            'Got total {:d} new proposals'.format(
                recent_talks.count() + recent_tutorials.count()
            ))

        if recent_talks:
            self.stdout.write('\n\nTalks:')
            self.proposal_summary(recent_talks)

        if recent_tutorials:
            self.stdout.write('\n\nTutorials:')
            self.proposal_summary(recent_tutorials)

    def cry(self):
        self.stderr.write(self.style.NOTICE(
            'No proposals are recently submitted. How come ...'
        ))

    def proposal_summary(self, queryset):
        table = []
        for p in queryset:
            table.append((
                str_stripper(p.get_category_display(), 16),
                str_stripper(p.get_python_level_display(), 16),
                p.title
            ))
        self.stdout.write(tabulate(
            table,
            ['Category', 'Python Level', 'Title'],
            tablefmt='simple'
        ))

