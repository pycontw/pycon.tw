from django import forms
from django.utils.translation import ugettext_lazy as _

from core.forms import RequestUserValidationMixin
from core.widgets import CharacterCountedTextarea, SimpleMDEWidget
from proposals.models import TalkProposal, TutorialProposal


class RequestUserSpeakerValidationMixin(RequestUserValidationMixin):
    """Mixin providing ``self._request`` and auth validation on cleaning.
    """
    error_messages = RequestUserValidationMixin.error_messages.copy()
    error_messages['bad_speaker'] = _(
        'Only authenticated user with complete speaker profile may '
        'create a {model_name}.'
    )

    def clean(self):
        """Validate user for saving later.
        """
        self.cleaned_data = super().clean()
        user = self._request.user
        if user.is_anonymous() or not user.is_valid_speaker():
            raise forms.ValidationError(self.get_error_message('bad_speaker'))
        return self.cleaned_data


class TalkProposalMixin:
    """Provide metadata for talk proposal forms.
    """
    class Meta:
        model = TalkProposal
        widgets = {
            'abstract': CharacterCountedTextarea(),
            'objective': CharacterCountedTextarea(),
            'detailed_description': SimpleMDEWidget(),
            'outline': SimpleMDEWidget(),
            'supplementary': SimpleMDEWidget(),
        }
        help_texts = {
            'objective': _(
                "<p><a href='#' data-toggle='modal' "
                "data-target='#proposalFieldExampleModal' "
                "data-content='objective'>Proposal Examples</a></p>"
                "Who is the intended audience for your talk? (Be specific, "
                "\"Python users\" is not a good answer). "
                "And what will the attendees get out of your talk? When they "
                "leave the room, what will they learn that they didn't know "
                "before? This is NOT made public and for REVIEW ONLY."
            ),
            'supplementary': _(
                "Anything else you'd like the program committee to know when "
                "making their selection: your past speaking experience, "
                "community experience, etc. This is NOT made public and for "
                "REVIEW ONLY. Edit using "
                "<a href='http://daringfireball.net/projects/markdown/basics' "
                "target='_blank' rel='noopener'>Markdown</a>."
            ),
            'outline': _(
                "<p><a href='#' data-toggle='modal' "
                "data-target='#proposalFieldExampleModal' "
                "data-content='outline'>Proposal Examples</a></p>"
                "How the talk will be arranged. It is highly recommended to "
                "attach the estimated time length for each sections in the "
                "talk. Talks in favor of 45min should have a fallback plan "
                "about how to shrink the content into a 30min one. Edit using "
                "<a href='http://daringfireball.net/projects/markdown/basics' "
                "target='_blank' rel='noopener'>Markdown</a>. "
                "This is NOT made public and for REVIEW ONLY."
            ),
        }


class TutorialProposalMixin:
    """Provide metadata for tutorial proposal forms.
    """
    class Meta:
        model = TutorialProposal
        widgets = {
            'abstract': CharacterCountedTextarea(),
            'objective': CharacterCountedTextarea(),
            'detailed_description': SimpleMDEWidget(),
            'outline': SimpleMDEWidget(),
            'supplementary': SimpleMDEWidget(),
        }
        help_texts = {
            'objective': _(
                "<p><a href='#' data-toggle='modal' "
                "data-target='#proposalFieldExampleModal' "
                "data-content='objective'>Proposal Examples</a></p>"
                "Who is the intended audience for your talk? (Be specific, "
                "\"Python users\" is not a good answer). "
                "And what will the attendees get out of your talk? When they "
                "leave the room, what will they learn that they didn't know "
                "before? This is NOT made public and for REVIEW ONLY."
            ),
            'supplementary': _(
                "Anything else you'd like the program committee to know when "
                "making their selection: your past speaking experience, "
                "community experience, etc. This is NOT made public and for "
                "REVIEW ONLY. Edit using "
                "<a href='http://daringfireball.net/projects/markdown/basics' "
                "target='_blank' rel='noopener'>Markdown</a>."
            ),
            'outline': _(
                "How the tutorial will be arranged. You should enumerate over "
                "each section in your talk and attach each section with the "
                "estimated time length. Edit using "
                "<a href='http://daringfireball.net/projects/markdown/basics' "
                "target='_blank' rel='noopener'>Markdown</a>. "
                "This is NOT made public and for REVIEW ONLY."
            ),
        }
