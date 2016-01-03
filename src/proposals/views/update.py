from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.html import format_html
from django.utils.translation import ugettext
from django.views.generic import UpdateView

from proposals.forms import TalkProposalUpdateForm, TutorialProposalUpdateForm
from proposals.models import TalkProposal, TutorialProposal

from .mixins import FormValidMessageMixin, UserProfileRequiredMixin


class ProposalUpdateView(
        LoginRequiredMixin, UserProfileRequiredMixin,
        FormValidMessageMixin, UpdateView):

    success_url = reverse_lazy('user_dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(submitter=self.request.user)


class TalkProposalUpdateView(ProposalUpdateView):

    model = TalkProposal
    form_class = TalkProposalUpdateForm
    template_name = 'proposals/talk_proposal_update.html'

    def get_form_valid_message(self):
        msg = ugettext('Talk proposal <strong>{title}</strong> updated.')
        return format_html(msg, title=self.object.title)


class TutorialProposalUpdateView(ProposalUpdateView):

    model = TutorialProposal
    form_class = TutorialProposalUpdateForm
    template_name = 'proposals/tutorial_proposal_update.html'

    def get_form_valid_message(self):
        msg = ugettext('Tutorial proposal <strong>{title}</strong> updated.')
        return format_html(msg, title=self.object.title)
