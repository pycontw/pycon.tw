from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from core.widgets import SimpleMDEWidget

from .models import AdditionalSpeaker, TalkProposal, TutorialProposal


User = get_user_model()


class OwnedByRequestUserMixin:
    """Mixin providing ``self._request`` and auth validation on cleaning.
    """
    error_messages = {
        'no_request': _(
            '{model_name_cap} creation requires a request object.'
        ),
        'bad_speaker': _(
            'Only authenticated user with complete speaker profile may '
            'create a {model_name}.'
        ),
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request

    def clean(self):
        """Validate user for saving later.
        """
        if self._request is None:
            raise forms.ValidationError(self.get_error_message('no_request'))
        user = self._request.user
        if user.is_anonymous() or not user.is_valid_speaker():
            raise forms.ValidationError(self.get_error_message('bad_speaker'))
        return self.cleaned_data

    def get_error_message(self, key):
        model_name = self._meta.model._meta.verbose_name
        return self.error_messages[key].format(
            model_name=model_name,
            model_name_cap=model_name.capitalize(),
        )


class AdditionalSpeakerCreateForm(OwnedByRequestUserMixin, forms.ModelForm):
    """Form used to add an additional speaker to a proposal.
    """
    email = forms.EmailField(
        label=_('speaker email'),
        help_text=_(
            'The speaker should have a registered account to tw.pycon.org, '
            'and have completed both email validation and the speaker profile.'
        ),
    )

    error_messages = OwnedByRequestUserMixin.error_messages.copy()
    error_messages.update({
        'bad_speaker': _(
            'Only authenticated user with complete speaker profile may '
            'create an {model_name}.'
        ),
        'no_proposal': _(
            'Additional speaker creation requires a proposal instance.'
        ),
        'not_owned_proposal': _(
            'User can only add additional speakers to owned proposals.'
        ),
        'duplicate_speaker': _(
            'This user is already a speaker for the proposal.'
        ),
        'invalid_user': _('No valid speaker found with your selection.'),
    })

    class Meta:
        model = AdditionalSpeaker
        fields = []

    def __init__(self, proposal=None, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        if self.instance.pk is not None:
            raise ValueError(
                'Additional speaker creation form cannot be used '
                'with an instance.'
            )
        self._proposal = proposal

    def clean_email(self):
        """Validate email attributes for saving later.

        The proposal submitter cannot be added as an additional speaker. A
        duplicate user cannot be added again.
        """
        proposal = self._proposal

        # Note that we can't do this in "clean" because the rest of this
        # method would fail when self._proposal is None.
        if not proposal:
            raise forms.ValidationError(self.get_error_message('no_proposal'))

        email = self.cleaned_data['email']
        try:
            user = User.objects.get_valid_speakers().get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(self.get_error_message('invalid_user'))

        # The rest of the validation is ordered this way to minimize queries
        # on valid data.

        # The user cannot already be one of the speakers.
        if (proposal.submitter == user
                or proposal.additional_speaker_set.filter(
                    cancelled=False, user=user).exists()):
            raise forms.ValidationError(
                self.get_error_message('duplicate_speaker'),
            )

        self._user = user
        return email

    def clean(self):
        """Validate proposal ownership for saving later.

        Only proposal owned by the current user may be added additional
        speakers.
        """
        cleaned_data = super().clean()
        if self._proposal.submitter != self._request.user:
            raise forms.ValidationError(
                self.get_error_message('not_owned_proposal'),
            )
        return cleaned_data

    def save(self, commit=True):
        try:
            speaker = self._proposal.additional_speaker_set.get(
                user=self._user, cancelled=True,
            )
        except self._meta.model.DoesNotExist:
            # No matching speaker -- good, just perform normal saving.
            speaker = super().save(commit=False)
            speaker.user = self._user
            speaker.proposal = self._proposal
        else:
            # If there is already a cancelled speaker matching this one,
            # reuse it without saving a new entry.
            speaker.cancelled = False

        if commit:
            speaker.save()
        return speaker


class AdditionalSpeakerUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance:
            raise ValueError(
                'Additional speaker update form must be initialized '
                'with an instance.'
            )


class AdditionalSpeakerCancelForm(AdditionalSpeakerUpdateForm):
    class Meta:
        model = AdditionalSpeaker
        fields = ['cancelled']


class AdditionalSpeakerSetStatusForm(AdditionalSpeakerUpdateForm):
    class Meta:
        model = AdditionalSpeaker
        fields = ['status']


class ProposalCreateForm(OwnedByRequestUserMixin, forms.ModelForm):
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
