from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.utils.html import format_html
from django.utils.translation import gettext
from django.views.generic import CreateView

from registry.helper import reg

from core.mixins import FormValidMessageMixin
from proposals.forms import TalkProposalCreateForm, TutorialProposalCreateForm

from .mixins import UserProfileRequiredMixin, CocAgreementMixin, ReviewsStateMixin


class ProposalCreateView(
        LoginRequiredMixin, UserProfileRequiredMixin,
        ReviewsStateMixin, FormValidMessageMixin, CocAgreementMixin,
        CreateView):

    def dispatch(self, request, *args, **kwargs):
        if not reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.proposals.creatable', False):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

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
        msg = gettext('Talk proposal <strong>{title}</strong> created.')
        return format_html(msg, title=self.object.title)


class TutorialProposalCreateView(ProposalCreateView):

    form_class = TutorialProposalCreateForm
    template_name = 'proposals/tutorial_proposal_create.html'

    def get_form_valid_message(self):
        msg = gettext('Tutorial proposal <strong>{title}</strong> created.')
        return format_html(msg, title=self.object.title)
