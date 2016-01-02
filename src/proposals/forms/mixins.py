from django import forms
from django.utils.translation import ugettext_lazy as _


class RequestUserSpeakerValidationMixin:
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
