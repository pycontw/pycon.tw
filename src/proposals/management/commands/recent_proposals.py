from datetime import datetime, timedelta
from io import StringIO

from tabulate import tabulate
import pytz
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q

from proposals.models import TalkProposal, TutorialProposal
from .slack import Slack

utc_tz = pytz.UTC
taiwan_tz = pytz.timezone('Asia/Taipei')


def str_stripper(s, max_len=32, ellipsis='...'):
    if len(s) > max_len:
        return s[:max_len - len(ellipsis)] + ellipsis
    else:
        return s


def proposal_summary(queryset):
    table = []
    for p in queryset:
        table.append((
            str_stripper(p.get_category_display(), 16),
            str_stripper(p.get_python_level_display(), 16),
            p.title
        ))
    return tabulate(
        table,
        ['Category', 'Python Level', 'Title'],
        tablefmt='simple'
    )


class Command(BaseCommand):
    help = "Summarize the recent proposal submits."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = StringIO()

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            metavar='N',
            type=int,
            default=3,
            help='Collect proposals submitted in the latest N days.'
        )
        parser.add_argument(
            '--hour',
            metavar='H',
            type=int,
            default=None,
            help="""
            Set the hour to cut the day shift. For example, if 21 O\'clock in
            is set, it finds proposals submitted between today-N 21:00 to today
            21:00. An error will be raised if the given hour time has not come.
            By default, it uses the nearest valid local (Asia/Taipei) hour.
            """
        )
        parser.add_argument(
            '--mailto',
            metavar='ADDR',
            type=str,
            action="append",
            default=None,
            help="""
            If set, mail the summary to the given address.
            Use --mailto multiple times to have more than one email receivers.
            """
        )
        parser.add_argument(
            '--slack',
            action='store_true',
            help="""
            Send the proposal to PyConTW Slack channel #program.
            If the settings `SLACK_WEBHOOK_URL` is not properly set, it will
            raise with an ImproperlyConfigured exception.
            """
        )

    def handle(self, *args, **options):
        """The command working logic"""
        recent_lookup, start_dt, end_dt = self.create_datetime_range_lookup(
            recent_days=options['days'], day_shift_hour=options['hour']
        )
        recent_talks = TalkProposal.objects.filter(recent_lookup)
        recent_tutorials = TutorialProposal.objects.filter(recent_lookup)
        if not recent_talks.exists() and not recent_tutorials.exists():
            self.cry()
        else:
            self.summary(recent_talks, recent_tutorials)
        self.msg.write(
            '\n\nGot total {:d} new proposals.\n'.format(
                recent_talks.count() + recent_tutorials.count()
            ))
        self.msg.write(
            'So far {:d} talk and {:d} tutorial proposals have been submitted.'
            .format(
                TalkProposal.objects.filter(cancelled=False).count(),
                TutorialProposal.objects.filter(cancelled=False).count()
            )
        )
        self.report(start_dt, end_dt, options['mailto'], options['slack'])
        self.msg.close()  # close the StringIO

    def summary(self, recent_talks, recent_tutorials):
        """Print out the proposal summary table"""
        if recent_talks:
            self.msg.write('\nTalks:\n\n')
            print(proposal_summary(recent_talks), file=self.msg)

        if recent_tutorials:
            self.msg.write('\nTutorials:\n\n')
            print(proposal_summary(recent_tutorials), file=self.msg)

    def report(self, start_dt, end_dt, mailto=None, slack=False):
        """Report to either the stdout or mailing to some address"""
        self.stdout.write(self.msg.getvalue())
        title = (
            'Proposal submission summary from {:%m/%d} to {:%m/%d}'
            .format(start_dt, end_dt)
        )
        if mailto:
            subject = '[PyConTW2016][Program] %s' % title
            send_mail(
                subject=subject,
                message=self.msg.getvalue(),
                from_email=None,
                recipient_list=mailto,
                fail_silently=False,
            )
        if slack:
            # Check if the slack integration is properly set
            if settings.SLACK_WEBHOOK_URL is None:
                raise ImproperlyConfigured("SLACK_WEBHOOK_URL is not set.")
            # Create the Slack client and send message
            slack = Slack(url=settings.SLACK_WEBHOOK_URL)
            status, msg = slack.notify(
                text='*%s*\n```\n%s\n```' % (title, self.msg.getvalue())
            )
            if status != 200:
                self.stderr.write(self.style.ERROR(
                    'Slack communication failed with status code %d (msg: %s)'
                    % (status, msg)
                ))

    def create_datetime_range_lookup(self, recent_days, day_shift_hour):
        """Create valid recent datetime range and return a lookup Q object"""
        if recent_days <= 0:
            raise CommandError(
                'Given number of days %d is not a positive number'
                % recent_days
            )
        today_utc_dt = utc_tz.fromutc(datetime.utcnow())
        if day_shift_hour is None:
            day_shift_hour = taiwan_tz.normalize(today_utc_dt).hour
        # To find the datetime range in Taiwan timezone
        #   today-N H:00 to today H:00
        try:
            today_dt = taiwan_tz.normalize(today_utc_dt).replace(
                hour=day_shift_hour, minute=0, second=0, microsecond=0
            )
        except ValueError as e:
            raise CommandError(
                'Given hour %d is invalid' % day_shift_hour
            ) from e
        if today_dt > today_utc_dt:
            raise CommandError(
                "Today's datetime {:%Y-%m-%d %H:%M} ({!s}) is yet present"
                .format(today_dt, taiwan_tz)
            )
        earliest_dt = today_dt - timedelta(days=recent_days)
        self.msg.write(
            'Proposals submitted during the recent {:d} days\n'
            'From {:%Y-%m-%d %H:%M} to {:%Y-%m-%d %H:%M}\n'
            '(Timezone: {!s})\n\n'
            .format(recent_days, earliest_dt, today_dt, taiwan_tz)
        )
        recent_lookup = Q(
            created_at__gte=earliest_dt,
            created_at__lt=today_dt,
            cancelled=False,
        )
        return recent_lookup, earliest_dt, today_dt

    def cry(self):
        self.msg.write(
            'No proposals are recently submitted\n'
            '◢▆▅▄▃ 崩╰(〒皿〒)╯潰 ▃▄▅▆◣\n'
        )
