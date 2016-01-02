from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.html import format_html
from django.utils.translation import ugettext
from django.views.generic import CreateView

from proposals.forms import TalkProposalCreateForm, TutorialProposalCreateForm

from .mixins import FormValidMessageMixin, UserProfileRequiredMixin


class ProposalCreateView(
        LoginRequiredMixin, UserProfileRequiredMixin,
        FormValidMessageMixin, CreateView):

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return self.object.get_update_url()


class TalkProposalCreateView(ProposalCreateView):

    form_class = TalkProposalCreateForm
    template_name = 'proposals/talk_proposal_create.html'

    def get_form_valid_message(self):
        msg = ugettext('Talk proposal <strong>{title}</strong> created.')
        return format_html(msg, title=self.object.title)


class TutorialProposalCreateView(ProposalCreateView):

    form_class = TutorialProposalCreateForm
    template_name = 'proposals/tutorial_proposal_create.html'

    def get_form_valid_message(self):
        msg = ugettext('Tutorial proposal <strong>{title}</strong> created.')
        return format_html(msg, title=self.object.title)
