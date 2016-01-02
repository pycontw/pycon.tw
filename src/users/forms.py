from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    ReadOnlyPasswordHashField,
)
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Fieldset, Layout, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users.

    Includes all the required fields, plus a repeated password.
    """
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.error_text_inline = False
        self.helper.attrs = {'autocomplete': 'off'}
        self.helper.label_class = 'sr-only'
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('email', placeholder=self.fields['email'].label),
                Field('password1', placeholder=self.fields['password1'].label),
                Field('password2', placeholder=self.fields['password2'].label),
            ),
            FormActions(
                Submit('save', _('Create Account'), css_class='btn-lg btn-block')
            )
        )

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        """Clean form email.

        :return str email: cleaned email
        :raise forms.ValidationError: Email is duplicated
        """
        # Since EmailUser.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        """Check that the two password entries match.

        :return str password2: cleaned password2
        :raise forms.ValidationError: password2 != password1
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True, auth=False):
        """Save user.

        Save the provided password in hashed format.

        :return users.models.EmailUser: user
        """
        if auth and not commit:
            raise ValueError(
                'Can not authenticate user without committing first.'
            )
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if not commit:
            return user
        user.save()
        if not auth:
            return user
        user = authenticate(
            email=self.cleaned_data['email'],
            password=password,
        )
        return user


class UserProfileUpdateForm(forms.ModelForm):
    """Form used to update user's profile.

    This includes only fields containing basic user information.
    """
    class Meta:
        model = User
        fields = ('speaker_name', 'bio', 'photo')


class AdminUserChangeForm(forms.ModelForm):
    """A form for updating users.

    Includes all the fields on the user, but replaces the password field
    with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>.")
    )

    class Meta:
        model = User
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        """Clean password.

        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value.

        :return str password:
        """
        return self.initial['password']


class AuthenticationForm(BaseAuthenticationForm):
    username = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.error_text_inline = False
        self.helper.label_class = 'sr-only'
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('username', placeholder=self.fields['username'].label),
                Field('password', placeholder=self.fields['password'].label),
            ),
            FormActions(
                Div(
                    Div(HTML('''<a class="btn btn-link">{btn_text}</a>'''.format(
                             btn_text=_('Forget Password?'))), css_class='col-xs-6 m-t-2'),
                    Div(Submit('save', _('Log In'), css_class='btn-lg btn-block'),
                        css_class='col-xs-6'),
                    css_class='row'
                    )
            )
        )
