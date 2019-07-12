import collections
import logging

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Count, Prefetch
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from core.mixins import FormValidMessageMixin
from core.utils import OrderedDefaultDict, TemplateExistanceStatusResponse
from proposals.models import AdditionalSpeaker, TalkProposal, TutorialProposal

from .forms import ScheduleCreationForm
from .models import (
    EVENT_ROOMS, Schedule, Time,
    CustomEvent, KeynoteEvent, SponsoredEvent,
    ProposedTalkEvent, ProposedTutorialEvent,
)
from .renderers import render_all


logger = logging.getLogger(__name__)


class AcceptedProposalMixin:
    def get_queryset(self):
        return (
            super().get_queryset()
            .filter_accepted()
            .annotate(_additional_speaker_count=Count('additionalspeaker_set'))
            .select_related('submitter')
        )


class TalkListView(AcceptedProposalMixin, ListView):

    model = TalkProposal
    template_name = 'events/talk_list.html'
    response_class = TemplateExistanceStatusResponse

    def get_categorized_talks(self):
        category_map = OrderedDefaultDict(list)
        proposals = (
            self.get_queryset()
            .prefetch_related(Prefetch(
                'additionalspeaker_set',
                queryset=(
                    AdditionalSpeaker.objects
                    .filter(cancelled=False)
                    .select_related('user')
                ),
                to_attr='_additional_speakers',
            ))
        )
        for proposal in proposals:
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
    response_class = TemplateExistanceStatusResponse

    def get(self, request, *args, **kwargs):
        try:
            self.schedule = Schedule.objects.latest()
        except Schedule.DoesNotExist:
            return HttpResponseRedirect(
                'https://docs.google.com/spreadsheets/d/e/'
                '2PACX-1vShbY20tmKca-i8Rzm4i2vaeifCHNCSM4e_'
                '6gfSykBzJMstMhsmxrNAFgIwezHkMCTUEgbUaL-DNHOD/pubhtml'
            )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            schedule_html=self.schedule.html,
            schedule_days=collections.OrderedDict([
                (key, {'name': value})
                for key, value in settings.EVENTS_DAY_NAMES.items()
            ]),
            **kwargs
        )


class ScheduleCreateMixin:

    form_class = ScheduleCreationForm
    form_valid_message = _('New talk schedule generated successfully.')
    permission_required = ['events.add_schedule']
    template_name = 'events/schedule_create.html'
    response_class = TemplateExistanceStatusResponse

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
        next(end_time_iter, None)

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
        with translation.override('en-us'):
            schedule_days = self.get_day_grouped_events()
        return super().get_context_data(
            schedule_days=schedule_days,
            **kwargs
        )


class EventInfoMixin:

    def is_event_sponsored(self):
        raise NotImplementedError

    def get_event(self):
        return self.object

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            sponsored=self.is_event_sponsored(),
            event=self.get_event(),
            **kwargs
        )


class ProposedEventMixin:

    event_model = None

    def is_event_sponsored(self):
        return False

    def get_event(self):
        try:
            event = (
                self.event_model.objects
                .select_related('begin_time', 'end_time')
                .get(proposal=self.object)
            )
        except self.event_model.DoesNotExist:
            return None
        return event


class TalkDetailView(
        AcceptedProposalMixin, ProposedEventMixin,
        EventInfoMixin, DetailView):
    model = TalkProposal
    event_model = ProposedTalkEvent
    template_name = 'events/talk_detail.html'
    response_class = TemplateExistanceStatusResponse


class SponsoredEventDetailView(EventInfoMixin, DetailView):

    model = SponsoredEvent
    template_name = 'events/sponsored_event_detail.html'
    response_class = TemplateExistanceStatusResponse

    def get_queryset(self):
        """Fetch user relation before-hand because we'll need it.
        """
        return super().get_queryset().select_related(
            'host', 'begin_time', 'end_time',
        )

    def is_event_sponsored(self):
        return True

    def get_time_slot(self):
        return (self.object.begin_time.value, self.object.end_time.value)


class TutorialDetailView(
        AcceptedProposalMixin, ProposedEventMixin,
        EventInfoMixin, DetailView):
    model = TutorialProposal
    event_model = ProposedTutorialEvent
    template_name = 'events/tutorial_detail.html'
    response_class = TemplateExistanceStatusResponse
