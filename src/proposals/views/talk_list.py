from django.views.generic import TemplateView
from proposals.models import TalkProposal


class TalkProposalListView(TemplateView):

    template_name = 'proposals/talk_proposal_list.html'

    def get_context_data(self, **kwargs):
        context = super(TalkProposalListView, self).get_context_data(**kwargs)
        accepted_talks = TalkProposal.objects.filter(accepted=True)
        context['object_list'] = accepted_talks
        return context

