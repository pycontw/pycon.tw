from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from django.views.generic import CreateView, UpdateView, TemplateView

from .forms import (
    TalkProposalCreateForm, TalkProposalUpdateForm, TalkProposalCancelForm,
    TutorialProposalCreateForm, TutorialProposalUpdateForm,
    TutorialProposalCancelForm,
)
from .models import TalkProposal, TutorialProposal


class UserProfileRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_anonymous() or not user.profile_filled:
            raise PermissionDenied
        return True


class ProposalCreateChoiceView(
        LoginRequiredMixin, UserProfileRequiredMixin, TemplateView):
    template_name = 'proposals/create_proposal_choice.html'


class FormValidMessageMixin:

    form_valid_message_level = messages.SUCCESS
    form_valid_message = None

    def get_form_valid_message_level(self):
        return self.form_valid_message_level

    def get_form_valid_message(self):
        return self.form_valid_message

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request,
            self.get_form_valid_message_level(),
            self.get_form_valid_message(),
        )
        return response


class ProposalCreateView(
        LoginRequiredMixin, UserProfileRequiredMixin,
        FormValidMessageMixin, CreateView):

    success_url_name = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse(self.success_url_name, kwargs={'pk': self.object.pk})


class TalkProposalCreateView(ProposalCreateView):

    form_class = TalkProposalCreateForm
    template_name = 'proposals/talk_proposal_create.html'
    success_url_name = 'talk_proposal_update'

    def get_form_valid_message(self):
        msg = ugettext('Talk proposal <strong>{title}</strong> created.')
        return mark_safe(msg.format(title=self.object.title))


class TutorialProposalCreateView(ProposalCreateView):

    form_class = TutorialProposalCreateForm
    template_name = 'proposals/tutorial_proposal_create.html'
    success_url_name = 'tutorial_proposal_update'

    def get_form_valid_message(self):
        msg = ugettext('Tutorial proposal <strong>{title}</strong> created.')
        return mark_safe(msg.format(title=self.object.title))


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
        return mark_safe(msg.format(title=self.object.title))


class TutorialProposalUpdateView(ProposalUpdateView):

    model = TutorialProposal
    form_class = TutorialProposalUpdateForm
    template_name = 'proposals/tutorial_proposal_update.html'

    def get_form_valid_message(self):
        msg = ugettext('Tutorial proposal <strong>{title}</strong> updated.')
        return mark_safe(msg.format(title=self.object.title))


class ProposalCancelView(ProposalUpdateView):
    http_method_names = ['post', 'options']
    form_valid_message_level = messages.INFO


class TalkProposalCancelView(ProposalCancelView):

    model = TalkProposal
    form_class = TalkProposalCancelForm

    def get_form_valid_message_level(self):
        if self.object.cancelled:
            return messages.INFO
        return messages.SUCCESS

    def get_form_valid_message(self):
        if self.object.cancelled:
            msg = ugettext(
                'Talk proposal <strong>{title}</strong> withdrawn.',
            )
        else:
            msg = ugettext(
                'Talk proposal <strong>{title}</strong> reactivated.',
            )
        return mark_safe(msg.format(title=self.object.title))


class TutorialProposalCancelView(ProposalCancelView):

    model = TutorialProposal
    form_class = TutorialProposalCancelForm

    def get_form_valid_message_level(self):
        if self.object.cancelled:
            return messages.INFO
        return messages.SUCCESS

    def get_form_valid_message(self):
        if self.object.cancelled:
            msg = ugettext(
                'Tutorial proposal <strong>{title}</strong> withdrawn.',
            )
        else:
            msg = ugettext(
                'Tutorial proposal <strong>{title}</strong> reactivated.',
            )
        return mark_safe(msg.format(title=self.object.title))
