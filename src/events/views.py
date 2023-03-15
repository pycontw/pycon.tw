import logging

from django.db.models import Count, Prefetch
from django.views.generic import DetailView, ListView

from core.utils import OrderedDefaultDict, TemplateExistanceStatusResponse
from proposals.models import AdditionalSpeaker, TalkProposal, TutorialProposal

from .models import ProposedTalkEvent, ProposedTutorialEvent, SponsoredEvent

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


class TutorialListView(ListView):
    model = ProposedTutorialEvent
    template_name = 'events/tutorial_list.html'
    response_class = TemplateExistanceStatusResponse

    def get_queryset(self):
        qs = (
            super().get_queryset()
            .filter(proposal__in=TutorialProposal.objects.filter_accepted())
            .order_by('begin_time', 'end_time', 'location')
            .select_related('proposal', 'proposal__submitter')
        )
        return qs


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

    def get_context_data(self, **kwargs):
        community_track_event = None

        return super().get_context_data(
            community_track_event=community_track_event,
            **kwargs,
        )


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

    def get_context_data(self, **kwargs):
        community_track_event = None

        return super().get_context_data(
            community_track_event=community_track_event,
            **kwargs,
        )


class TutorialDetailView(
        AcceptedProposalMixin, ProposedEventMixin,
        EventInfoMixin, DetailView):
    model = TutorialProposal
    event_model = ProposedTutorialEvent
    template_name = 'events/tutorial_detail.html'
    response_class = TemplateExistanceStatusResponse
