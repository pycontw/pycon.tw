from django import forms

from core.widgets import SimpleMDEWidget
from .models import TalkProposal


class TalkProposalCreateForm(forms.ModelForm):
    """Form used to create a proposal.

    Fields in this form is intentionally reduced to allow people to submit
    a proposal very quickly, and fill in the details later.
    """
    class Meta:
        model = TalkProposal
        fields = [
            'title', 'category', 'duration', 'language',
            'python_level', 'recording_policy',
        ]

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request

    def clean(self):
        """Validate user for saving later.

        Only a valid user with filled profile may create a proposal.
        """
        if self._request is None:
            raise forms.ValidationError(
                'Talk proposal creation requires a request object.'
            )
        user = self._request.user
        if user.is_anonymous() or not user.profile_filled:
            raise forms.ValidationError(
                'Only authenticated user with complete speaker profile may '
                'submit a proposal.'
            )
        return self.cleaned_data

    def save(self, commit=True):
        """Fill user field on save.
        """
        proposal = super().save(commit=False)
        proposal.submitter = self._request.user
        if commit:
            proposal.save()
        return proposal


class TalkProposalUpdateForm(forms.ModelForm):
    """Form used to update a proposal.

    This is the complete editing form for proposal. It should contain all
    user-editable fields.
    """
    class Meta:
        model = TalkProposal
        fields = [
            'title', 'category', 'duration', 'language', 'target_audience',
            'abstract', 'python_level', 'detailed_description', 'outline',
            'supplementary', 'recording_policy', 'slide_link',
        ]
        widgets = {
            'detailed_description': SimpleMDEWidget(),
            'outline': SimpleMDEWidget(),
            'supplementary': SimpleMDEWidget(),
        }
