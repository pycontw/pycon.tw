from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from proposals.models import AdditionalSpeaker

from .mixins import RequestUserSpeakerValidationMixin


User = get_user_model()


class AdditionalSpeakerCreateForm(
        RequestUserSpeakerValidationMixin, forms.ModelForm):
    """Form used to add an additional speaker to a proposal.
    """
    email = forms.EmailField(
        label=_('speaker email'),
        help_text=_(
            'The speaker should have a registered account to tw.pycon.org, '
            'and have completed both email validation and the speaker profile.'
        ),
    )

    error_messages = RequestUserSpeakerValidationMixin.error_messages.copy()
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
                or proposal.additionalspeaker_set.filter(
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
            speaker = self._proposal.additionalspeaker_set.get(
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
