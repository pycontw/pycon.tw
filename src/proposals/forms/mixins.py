from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from core.forms import RequestUserValidationMixin
from core.utils import format_html_lazy
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
        if user.is_anonymous or not user.is_valid_speaker():
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
            'abstract': _(
                "<p><a href='#' data-toggle='modal' "
                "data-target='#proposalFieldExampleModal' "
                "data-content='abstract'>Proposal Examples</a>.</p>"
                "<p>The overview of what the talk is about. If the talk "
                "assume some domain knowledge please state it here. If your "
                "talk is accepted, this will be displayed on both the website "
                "and the handbook. Should be one paragraph.</p>"
            ),
            'python_level': format_html_lazy(
                _("The choice of talk level matters during the review "
                  "process. More definition of talk level can be found at the "
                  "<a href='{speaking_talk_url}' target='_blank'>"
                  "How to Propose a Talk</a> page. Note that a proposal won't "
                  "be more likely to be accepted because of being 'Novice' "
                  "level. We may contact you to change the talk level when "
                  "we find the content is too-hard or too-easy for the "
                  "target audience."),
                speaking_talk_url=reverse_lazy(
                    'page', kwargs={'path': 'speaking/talk'},
                ),
            ),
            'detailed_description': _(
                "<p><a href='#' data-toggle='modal' "
                "data-target='#proposalFieldExampleModal' "
                "data-content='detailed description'>"
                "Proposal Examples</a>.</p>"
                "<p>Try not be too lengthy to scare away reviewers or "
                "potential audience. A comfortable length is less than 2000 "
                "characters (or about 1200 Chinese characters). Since most "
                "reviewers may not understand the topic as deep as you do, "
                "including related links to the talk topic will help "
                "reviewers understand the proposal. Edit using "
                "<a href='http://daringfireball.net/projects/markdown/basics' "
                "target='_blank' rel='noopener'>Markdown</a>."
            ),
            'recording_policy': format_html_lazy(
                _("Whether you agree to give permission to PyCon Taiwan to "
                  "record, edit, and release audio and video of your "
                  "presentation. More information can be found at "
                  "<a href='{recording_policy_url}' target='_blank'>"
                  "Recording Release</a> page."),
                recording_policy_url=reverse_lazy(
                    'page', kwargs={'path': 'speaking/recording'},
                )
            ),
            'slide_link': _(
                "You can add your slide link near or after the conference "
                "day. Not required for review."
            ),
            'objective': _(
                "<p><a href='#' data-toggle='modal' "
                "data-target='#proposalFieldExampleModal' "
                "data-content='objective'>Proposal Examples</a>.</p>"
                "<p>Who is the intended audience for your talk? (Be specific, "
                "\"Python users\" is not a good answer). "
                "And what will the attendees get out of your talk? When they "
                "leave the room, what will they learn that they didn't know "
                "before? This is NOT made public and for REVIEW ONLY.</p>"
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
                "data-content='outline'>Proposal Examples</a>.</p>"
                "<p>How the talk will be arranged. It is highly recommended "
                "to attach the estimated time length for each sections in the "
                "talk. Talks in favor of 45min should have a fallback plan "
                "about how to shrink the content into a 30min one. Edit using "
                "<a href='http://daringfireball.net/projects/markdown/basics' "
                "target='_blank' rel='noopener'>Markdown</a>. "
                "This is NOT made public and for REVIEW ONLY.</p>"
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
            'abstract': _(
                "<p><a href='#' data-toggle='modal' "
                "data-target='#proposalFieldExampleModal' "
                "data-content='abstract'>Proposal Examples</a>.</p>"
                "<p>The overview of what the talk is about. If the talk "
                "assume some domain knowledge please state it here. If your "
                "talk is accepted, this will be displayed on both the website "
                "and the handbook. Should be one paragraph.</p>"
            ),
            'python_level': format_html_lazy(
                _("The choice of talk level matters during the review "
                  "process. More definition of talk level can be found at the "
                  "<a href='{speaking_talk_url}' target='_blank'>"
                  "How to Propose a Talk</a> page. Note that a proposal won't "
                  "be more likely to be accepted because of being 'Novice' "
                  "level. We may contact you to change the talk level when "
                  "we find the content is too-hard or too-easy for the "
                  "target audience."),
                speaking_talk_url=reverse_lazy(
                    'page', kwargs={'path': 'speaking/talk'},
                ),
            ),
            'detailed_description': _(
                "<p><a href='#' data-toggle='modal' "
                "data-target='#proposalFieldExampleModal' "
                "data-content='detailed description'>"
                "Proposal Examples</a>.</p>"
                "<p>Try not be too lengthy to scare away reviewers or "
                "potential audience. A comfortable length is less than 2000 "
                "characters (or about 1200 Chinese characters). Since most "
                "reviewers may not understand the topic as deep as you do, "
                "including related links to the talk topic will help "
                "reviewers understand the proposal. Edit using "
                "<a href='http://daringfireball.net/projects/markdown/basics' "
                "target='_blank' rel='noopener'>Markdown</a>."
            ),
            'recording_policy': format_html_lazy(
                _("Whether you agree to give permission to PyCon Taiwan to "
                  "record, edit, and release audio and video of your "
                  "presentation. More information can be found at "
                  "<a href='{recording_policy_url}' target='_blank'>"
                  "Recording Release</a> page."),
                recording_policy_url=reverse_lazy(
                    'page', kwargs={'path': 'speaking/recording'},
                )
            ),
            'slide_link': _(
                "You can add your slide link near or after the conference "
                "day. Not required for review."
            ),
            'objective': _(
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
