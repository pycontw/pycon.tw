from django.conf import settings
from django.contrib import messages
from django.utils.html import format_html
from django.utils.translation import ugettext

from proposals.forms import TalkProposalCancelForm, TutorialProposalCancelForm
from proposals.models import TalkProposal, TutorialProposal

from .update import ProposalUpdateView


class ProposalCancelView(ProposalUpdateView):

    http_method_names = ['post', 'options']
    form_valid_message_level = messages.INFO

    def can_edit(self):
        return settings.PROPOSALS_WITHDRAWABLE


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
        return format_html(msg, title=self.object.title)


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
        return format_html(msg, title=self.object.title)
