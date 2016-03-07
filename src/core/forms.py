from django import forms
from django.utils.translation import ugettext_lazy as _


class RequestUserValidationMixin:
    """Mixin providing ``self._request`` and validation on cleaning.
    """
    error_messages = {
        'no_request': _(
            '{model_name_cap} creation requires a request object.'
        ),
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request

    def clean(self):
        if self._request is None:
            raise forms.ValidationError(self.get_error_message('no_request'))
        return self.cleaned_data

    def get_error_message(self, key):
        model_name = self._meta.model._meta.verbose_name
        return self.error_messages[key].format(
            model_name=model_name,
            model_name_cap=model_name.capitalize(),
        )
