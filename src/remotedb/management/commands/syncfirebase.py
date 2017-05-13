import itertools

from firebase.firebase import FirebaseApplication

from django.conf import settings
from django.core.management.base import BaseCommand

from events.models import (
    CustomEvent, KeynoteEvent, ProposedTalkEvent, SponsoredEvent,
)
from remotedb import dumpers


class Command(BaseCommand):

    help = 'Sync Firebase instance with local data.'

    def handle(self, *args, **options):
        custeom_event_qs = (
            CustomEvent.objects
            .select_related('begin_time', 'end_time')
        )
        keynote_event_qs = (
            KeynoteEvent.objects
            .select_related('begin_time', 'end_time')
        )
        proposed_talk_event_qs = (
            ProposedTalkEvent.objects
            .select_related('begin_time', 'end_time', 'proposal__submitter')
        )
        sponsored_event_qs = (
            SponsoredEvent.objects
            .select_related('begin_time', 'end_time', 'host')
        )

        self.stdout.write('Dumping schedule...', ending=' ')
        schedule_data = dumpers.dump_schedule(itertools.chain(
            custeom_event_qs,
            keynote_event_qs,
            proposed_talk_event_qs,
            sponsored_event_qs,
        ))
        self.stdout.write('Done')

        self.stdout.write('Dumping event details...', ending=' ')
        event_data = {
            str(event.proposal.pk): dumpers.dump_proposal(event.proposal)
            for event in proposed_talk_event_qs
        }
        event_data.update({
            'sponsored_{}'.format(e.pk): dumpers.dump_sponsored_event_detail(e)
            for e in sponsored_event_qs
        })
        self.stdout.write('Done')

        app = FirebaseApplication(settings.FIREBASE_URL)

        self.stdout.write('Uploading schedule...', ending=' ')
        for key, value in schedule_data.items():
            self.stdout.write(key, ending=' ')
            data = {'date': key, 'slots': value}
            app.put('{}/schedule'.format(settings.FIREBASE_DB), key, data)
        self.stdout.write('Done')

        self.stdout.write('Uploading events...', ending=' ')
        app.put(settings.FIREBASE_DB, 'events', event_data)
        self.stdout.write('Done')
