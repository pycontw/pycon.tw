from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.html import format_html
from django.utils.translation import ugettext
from django.views.generic import UpdateView

from core.mixins import FormValidMessageMixin
from proposals.forms import TalkProposalUpdateForm, TutorialProposalUpdateForm
from proposals.models import TalkProposal, TutorialProposal
from reviews.models import Review

from .mixins import (
    ProposalEditMixin, ProposalExamplesMixin, UserProfileRequiredMixin,
)


class TalkProposalMixin:

    model = TalkProposal
    form_class = TalkProposalUpdateForm

    def get_reviews(self):
        review_iter = (
            Review.objects
            .filter_current_reviews(proposal=self.object)
            .filter(appropriateness=True, discloses_comment=True)
            .iter_reviewer_latest_reviews()
        )
        return sorted(review_iter, key=lambda r: Review.VOTE_ORDER[r.vote])

    def get_context_data(self, **kwargs):
        reviews = self.get_reviews()

        context = super().get_context_data(**kwargs)
        context.update({'reviews': reviews})
        return context


class TutorialProposalMixin:
    model = TutorialProposal
    form_class = TutorialProposalUpdateForm


class ProposalUpdateView(
        LoginRequiredMixin, UserProfileRequiredMixin,
        ProposalEditMixin, ProposalExamplesMixin,
        FormValidMessageMixin, UpdateView):

    success_url = reverse_lazy('user_dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(submitter=self.request.user)


class TalkProposalUpdateView(TalkProposalMixin, ProposalUpdateView):

    template_name = 'proposals/talk_proposal_update.html'

    def get_form_valid_message(self):
        msg = ugettext('Talk proposal <strong>{title}</strong> updated.')
        return format_html(msg, title=self.object.title)


class TutorialProposalUpdateView(TutorialProposalMixin, ProposalUpdateView):

    template_name = 'proposals/tutorial_proposal_update.html'

    def get_form_valid_message(self):
        msg = ugettext('Tutorial proposal <strong>{title}</strong> updated.')
        return format_html(msg, title=self.object.title)


class ReadonlyProposalUpdateView(
        LoginRequiredMixin, UserProfileRequiredMixin,
        FormValidMessageMixin, UpdateView):

    http_method_names = ['get', 'options']

    def get_queryset(self):
        return super().get_queryset().filter_viewable(self.request.user)

    def get_form(self):
        form = super().get_form()
        for field in form.fields.values():
            field.disabled = True
            field.help_text = ''
        return form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['readonly'] = True
        return data


class ReadonlyTalkProposalUpdateView(
        TalkProposalMixin, ReadonlyProposalUpdateView):
    template_name = 'proposals/talk_proposal_peek.html'


class ReadonlyTutorialProposalUpdateView(
        TutorialProposalMixin, ReadonlyProposalUpdateView):
    template_name = 'proposals/tutorial_proposal_peek.html'
