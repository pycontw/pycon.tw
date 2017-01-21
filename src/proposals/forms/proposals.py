from django import forms
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper

from core.utils import form_has_instance
from core.widgets import CharacterCountedTextarea, SimpleMDEWidget
from proposals.models import TalkProposal, TutorialProposal

from .mixins import RequestUserSpeakerValidationMixin


class ProposalCreateForm(RequestUserSpeakerValidationMixin, forms.ModelForm):
    """Form used to create a proposal.

    Fields in this form is intentionally reduced to allow people to submit
    a proposal very quickly, and fill in the details later.
    """
    def save(self, commit=True):
        """Fill user field on save.
        """
        proposal = super().save(commit=False)
        proposal.submitter = self._request.user
        if commit:
            proposal.save()
        return proposal


class TalkProposalCreateForm(ProposalCreateForm):

    duration = forms.ChoiceField(
        label=_('duration'),
        choices=(
            ('NOPREF', _('No preference')),
            ('PREF30', _('Prefer 30min')),
            ('PREF45', _('Prefer 45min')),
        ),
    )

    class Meta:
        model = TalkProposal
        fields = [
            'title', 'category', 'duration', 'language',
            'python_level', 'recording_policy',
        ]


class TutorialProposalCreateForm(ProposalCreateForm):
    class Meta:
        model = TutorialProposal
        fields = [
            'title', 'category', 'duration', 'language',
            'python_level', 'recording_policy',
        ]


class ProposalUpdateForm(forms.ModelForm):
    @cached_property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.include_media = False
        return helper


class TalkProposalUpdateForm(ProposalUpdateForm):
    """Form used to update a talk proposal.

    This is the complete editing form for proposal. It should contain all
    user-editable fields.
    """
    duration = forms.ChoiceField(
        label=_('duration'),
        choices=(
            ('NOPREF', _('No preference')),
            ('PREF30', _('Prefer 30min')),
            ('PREF45', _('Prefer 45min')),
        ),
    )

    class Meta:
        model = TalkProposal
        fields = [
            'title', 'category', 'duration', 'language',
            'abstract', 'python_level', 'objective', 'detailed_description',
            'outline', 'supplementary', 'recording_policy', 'slide_link',
        ]
        widgets = {
            'abstract': CharacterCountedTextarea(),
            'objective': CharacterCountedTextarea(),
            'detailed_description': SimpleMDEWidget(),
            'outline': SimpleMDEWidget(),
            'supplementary': SimpleMDEWidget(),
        }


class TutorialProposalUpdateForm(ProposalUpdateForm):
    """Form used to update a tutorial proposal.

    This is the complete editing form for proposal. It should contain all
    user-editable fields.
    """
    class Meta:
        model = TutorialProposal
        fields = [
            'title', 'category', 'duration', 'language',
            'abstract', 'python_level', 'objective', 'detailed_description',
            'outline', 'supplementary', 'recording_policy', 'slide_link',
        ]
        widgets = {
            'abstract': CharacterCountedTextarea(),
            'objective': CharacterCountedTextarea(),
            'detailed_description': SimpleMDEWidget(),
            'outline': SimpleMDEWidget(),
            'supplementary': SimpleMDEWidget(),
        }


class ProposalCancelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not form_has_instance(self):
            raise ValueError(
                'Proposal cancel form must be initialized with an instance.'
            )


class TalkProposalCancelForm(ProposalCancelForm):
    class Meta:
        model = TalkProposal
        fields = ['cancelled']


class TutorialProposalCancelForm(ProposalCancelForm):
    class Meta:
        model = TutorialProposal
        fields = ['cancelled']
