from django.views.generic import DetailView, ListView

from proposals.models import TalkProposal


class AcceptedTalkMixin:
    queryset = (
        TalkProposal.objects
        .filter(accepted=True).select_related('submitter')
        .order_by('title')
    )


class TalkListView(AcceptedTalkMixin, ListView):
    template_name = 'events/talk_list.html'


class TalkDetailView(AcceptedTalkMixin, DetailView):
    template_name = 'events/talk_detail.html'
