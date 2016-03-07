from django import forms
from django.utils.translation import ugettext_lazy as _

from core.forms import RequestUserValidationMixin


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
