from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .mixins import UserProfileRequiredMixin


class ProposalCreateChoiceView(
        LoginRequiredMixin, UserProfileRequiredMixin, TemplateView):
    template_name = 'proposals/create_proposal_choice.html'


from .cancel import TalkProposalCancelView, TutorialProposalCancelView  # noqa
from .create import TalkProposalCreateView, TutorialProposalCreateView  # noqa
from .update import TalkProposalUpdateView, TutorialProposalUpdateView  # noqa

from .speakers import (     # noqa
    AdditionalSpeakerRemoveView, AdditionalSpeakerSetStatusView,
    TalkProposalManageSpeakersView, TutorialProposalManageSpeakersView,
)
