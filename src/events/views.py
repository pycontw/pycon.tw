import collections
import logging

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, TemplateView

from core.mixins import FormValidMessageMixin
from core.utils import OrderedDefaultDict
from proposals.models import TalkProposal

from .forms import ScheduleCreationForm
from .models import (
    EVENT_ROOMS, Location, Schedule, Time,
    CustomEvent, KeynoteEvent, SponsoredEvent, ProposedTalkEvent,
)
from .renderers import render_all


logger = logging.getLogger(__name__)


class AcceptedTalkMixin:
    queryset = (
        TalkProposal.objects
        .filter_accepted()
        .annotate(_additional_speaker_count=Count('additionalspeaker_set'))
        .select_related('submitter')
    )


class TalkListView(AcceptedTalkMixin, TemplateView):

    template_name = 'events/talk_list.html'

    def get_categorized_talks(self):
        category_map = OrderedDefaultDict(list)
        for proposal in self.queryset:
            category_map[proposal.get_category_display()].append(proposal)
        return category_map

    def get_sponsored_talks(self):
        sponsored_events = (
            SponsoredEvent.objects
            .select_related('host')
            .order_by('title')
        )
        return sponsored_events

    def get_context_data(self, **kwargs):
        kwargs.update({
            'talk_category_list_pairs': self.get_categorized_talks().items(),
            'sponsored_events': self.get_sponsored_talks(),
        })
        return super().get_context_data(**kwargs)


class ScheduleView(TemplateView):

    template_name = 'events/schedule.html'

    def get(self, request, *args, **kwargs):
        try:
            self.schedule = Schedule.objects.latest()
        except Schedule.DoesNotExist:
            return HttpResponseRedirect(
                'https://docs.google.com/spreadsheets/d/'
                '17-8E1OhfgiG4pIOIrp3OpNY4OaK1QxUn4TJK9oVmRSw/htmlview',
            )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            schedule_html=self.schedule.html,
            days=settings.EVENTS_DAY_NAMES,
            **kwargs
        )


class ScheduleCreateMixin:

    form_class = ScheduleCreationForm
    form_valid_message = _('New talk schedule generated successfully.')
    permission_required = ['events.add_schedule']
    template_name = 'events/schedule_create.html'

    def get_success_url(self):
        return reverse('events_schedule')


class ScheduleCreate2016View(
        ScheduleCreateMixin, FormValidMessageMixin, PermissionRequiredMixin,
        CreateView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(content=render_all(), **kwargs)


class ScheduleCreateView(
        ScheduleCreateMixin, FormValidMessageMixin, PermissionRequiredMixin,
        CreateView):

    event_querysets = [
        CustomEvent.objects.all(),
        KeynoteEvent.objects.all(),
        (
            ProposedTalkEvent.objects
            .select_related('proposal__submitter')
            .annotate(_additional_speaker_count=Count(
                'proposal__additionalspeaker_set',
            ))
        ),
        SponsoredEvent.objects.select_related('host'),
    ]

    def get_day_grouped_events(self):
        begin_time_event_dict = collections.defaultdict(set)
        for qs in self.event_querysets:
            for event in qs.select_related('begin_time', 'end_time'):
                begin_time_event_dict[event.begin_time].add(event)

        day_info_dict = collections.OrderedDict(
            (date, {
                'name': name, 'rooms': set(),
                'slots': OrderedDefaultDict(dict),
            }) for date, name in settings.EVENTS_DAY_NAMES.items()
        )

        def room_key(room):
            return room.split('-', 1)[-1]

        times = list(Time.objects.order_by('value'))
        end_time_iter = iter(times)
        next(end_time_iter)
        for begin, end in zip(times, end_time_iter):
            try:
                day_info = day_info_dict[begin.value.date()]
            except KeyError:
                logger.warn('Invalid time sot dropped: {}'.format(begin))
                continue
            for event in begin_time_event_dict[begin]:
                location = event.location
                if location in EVENT_ROOMS:
                    day_info['rooms'].add(location)
                day_info['slots'][(begin, end)][location] = event

        for info in day_info_dict.values():
            # Sort rooms.
            info['rooms'] = sorted(info['rooms'], key=room_key)
            # Work around Django template unable to iter through defaultdict.
            # http://stackoverflow.com/questions/4764110
            info['slots'] = collections.OrderedDict(
                (slot_time, sorted(
                    slot_rooms.items(), key=lambda i: room_key(i[0])))
                for slot_time, slot_rooms in info['slots'].items()
            )

        return day_info_dict

    def get_context_data(self, **kwargs):
        schedule_days = self.get_day_grouped_events()
        return super().get_context_data(
            days=settings.EVENTS_DAY_NAMES,
            schedule_days=schedule_days,
            **kwargs
        )


class TalkDetailView(AcceptedTalkMixin, DetailView):
    template_name = 'events/talk_detail.html'


class SponsoredEventDetailView(DetailView):

    model = SponsoredEvent
    template_name = 'events/sponsored_event_detail.html'

    def get_queryset(self):
        """Fetch user relation before-hand because we'll need it.
        """
        return super().get_queryset().select_related('host')
