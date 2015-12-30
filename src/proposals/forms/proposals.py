from django import forms

from core.widgets import SimpleMDEWidget
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


class TalkProposalUpdateForm(forms.ModelForm):
    """Form used to update a talk proposal.

    This is the complete editing form for proposal. It should contain all
    user-editable fields.
    """
    class Meta:
        model = TalkProposal
        fields = [
            'title', 'category', 'duration', 'language', 'target_audience',
            'abstract', 'python_level', 'objective', 'detailed_description',
            'outline', 'supplementary', 'recording_policy', 'slide_link',
        ]
        widgets = {
            'detailed_description': SimpleMDEWidget(),
            'outline': SimpleMDEWidget(),
            'supplementary': SimpleMDEWidget(),
        }


class TutorialProposalUpdateForm(forms.ModelForm):
    """Form used to update a tutorial proposal.

    This is the complete editing form for proposal. It should contain all
    user-editable fields.
    """
    class Meta:
        model = TutorialProposal
        fields = [
            'title', 'category', 'duration', 'language', 'target_audience',
            'abstract', 'python_level', 'objective', 'detailed_description',
            'outline', 'supplementary', 'recording_policy', 'slide_link',
        ]
        widgets = {
            'detailed_description': SimpleMDEWidget(),
            'outline': SimpleMDEWidget(),
            'supplementary': SimpleMDEWidget(),
        }


class ProposalCancelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance:
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
