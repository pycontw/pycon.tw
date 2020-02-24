from django import forms
from django.utils.translation import gettext_lazy as _

from core.forms import RequestUserValidationMixin

from .models import REVIEW_REQUIRED_PERMISSIONS, Review


class ReviewForm(RequestUserValidationMixin, forms.ModelForm):

    error_messages = RequestUserValidationMixin.error_messages.copy()
    error_messages.update({
        'bad_reviewer': _(
            'The current user is invalid to create a {model_name}.'
        ),
        'no_proposal': _(
            '{model_name_cap} creation requires a proposal object.'
        ),
    })
    permission_required = REVIEW_REQUIRED_PERMISSIONS

    class Meta:
        model = Review
        fields = ['vote', 'comment', 'discloses_comment', 'note']

    def __init__(self, proposal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._proposal = proposal

    def clean(self):
        """Validate user and proposal for saving later.
        """
        self.cleaned_data = super().clean()
        user = self._request.user
        if not user.has_perms(self.permission_required):
            raise forms.ValidationError(self.get_error_message('bad_reviewer'))

        proposal = self._proposal
        if not proposal:
            raise forms.ValidationError(self.get_error_message('no_proposal'))
        proposal_available = (
            type(proposal).objects
            .filter_reviewable(user)
            .filter(pk=proposal.pk)
            .exists()
        )
        if not proposal_available:
            raise forms.ValidationError(
                _('Could not review proposal {proposal}.').format(
                    proposal=proposal,
                )
            )
        return self.cleaned_data

    def save(self, commit=True):
        review = super().save(commit=False)
        review.reviewer = self._request.user
        review.proposal = self._proposal
        if commit:
            review.save()
        return review
