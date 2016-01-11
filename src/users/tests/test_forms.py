import pytest

from crispy_forms.helper import FormHelper

from users.forms import PasswordResetForm, SetPasswordForm, UserCreationForm


@pytest.mark.parametrize('form_class,kwarg_keys', [
    (PasswordResetForm, []),
    (SetPasswordForm,   ['user']),
    (UserCreationForm,  []),
])
def test_form_helper(user, form_class, kwarg_keys):
    locs = locals()
    form = form_class(**{key: locs[key] for key in kwarg_keys})
    assert isinstance(form.helper, FormHelper)
