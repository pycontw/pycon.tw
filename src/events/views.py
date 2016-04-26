from django.views.generic import DetailView, ListView

from proposals.models import TalkProposal

from .models import SponsoredEvent


class AcceptedTalkMixin:
    queryset = (
        TalkProposal.objects
        .filter(accepted=True).select_related('submitter')
        .order_by('title')
    )


class TalkListView(AcceptedTalkMixin, ListView):

    template_name = 'events/talk_list.html'

    def get_context_data(self, **kwargs):
        sponsored_events = (
            SponsoredEvent.objects
            .select_related('host')
            .order_by('title')
        )
        return super().get_context_data(
            sponsored_events=sponsored_events,
            **kwargs
        )


class TalkDetailView(AcceptedTalkMixin, DetailView):
    template_name = 'events/talk_detail.html'


class SponsoredEventDetailView(DetailView):
    model = SponsoredEvent
    template_name = 'events/sponsored_event_detail.html'
