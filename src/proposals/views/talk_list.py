from django.views.generic import ListView

from proposals.models import TalkProposal


class TalkProposalListView(ListView):
    template_name = 'proposals/talk_proposal_list.html'
    queryset = (
        TalkProposal.objects
        .filter(accepted=True).select_related('submitter')
    )
