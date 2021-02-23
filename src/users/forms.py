from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm,
    ReadOnlyPasswordHashField,
)
from django.core.files.images import get_image_dimensions
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Fieldset, Layout, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions, InlineCheckboxes


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

    def save(self, commit=True):
        """Save user.

        Save the provided password in hashed format.

        :return users.models.EmailUser: user
        """
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user


class PublicUserCreationForm(UserCreationForm):
    """Form used to create new user through public interface.

    This inherits the basic user-creation form, but adds a form helper for
    layout, and provides option to log the user in automatically when calling
    ``save()``.
    """
    @cached_property
    def helper(self):
        helper = FormHelper()
        helper.error_text_inline = False
        helper.attrs = {
            'autocomplete': 'off', 'autocorrect': 'off',
            'autocapitalize': 'off', 'spellcheck': 'false',
        }
        helper.label_class = 'sr-only'
        helper.layout = Layout(
            Fieldset(
                '',
                Field('email', placeholder=self.fields['email'].label),
                Field('password1', placeholder=self.fields['password1'].label),
                Field('password2', placeholder=self.fields['password2'].label),
            ),
            FormActions(
                Submit(
                    'save', _('Create Account'), css_class='btn-lg btn-block',
                )
            )
        )
        return helper

    def save(self, commit=True, auth=True):
        """Save user.

        If `auth` is True, the user is automatically logged-in after saving.
        """
        if auth and not commit:
            raise ValueError(
                'Can not authenticate user without committing first.'
            )
        user = super().save(commit=commit)
        if auth:
            user = authenticate(
                email=self.cleaned_data['email'],
                password=self.cleaned_data.get('password1'),
            )
        return user


class UserProfileUpdateForm(forms.ModelForm):
    """Form used to update user's profile.

    This includes only fields containing basic user information.
    """
    error_messages = {
        'photo_too_small': _(
            'Your image is too small ({width}\u00d7{height} pixels).'
        ),
        'photo_bad_dimension': _('The image you provided is not quadrate.'),
        'photo_size_too_large': _('Your image size is too big (>10M)'),
    }

    class Meta:
        model = User
        fields = (
            'speaker_name', 'bio', 'photo',
            'facebook_profile_url', 'twitter_id', 'github_id',
        )

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            return photo

        try:
            width, height = get_image_dimensions(photo)
        except FileNotFoundError:
            width = height = 0
        if width < 800 or height < 800:
            raise forms.ValidationError(self.get_error_message(
                'photo_too_small', width=width, height=height,
            ))

        ratio = width / height
        if ratio < 0.9 or ratio > 1.1:
            raise forms.ValidationError(self.get_error_message(
                'photo_bad_dimension', width=width, height=height,
            ))

        if photo.size > 10 * 1024 ** 2:
            raise forms.ValidationError(self.get_error_message(
                'photo_size_too_large',
            ))
        return photo

    def get_error_message(self, *args, **kwargs):
        key, *args = args
        msg = self.error_messages[key]
        if args or kwargs:
            msg = msg.format(*args, **kwargs)
        return msg


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

    @cached_property
    def helper(self):
        helper = FormHelper()
        helper.error_text_inline = False
        helper.label_class = 'sr-only'
        helper.attrs = {
            'autocomplete': 'off', 'autocorrect': 'off',
            'autocapitalize': 'off', 'spellcheck': 'false',
        }
        helper.layout = Layout(
            Fieldset(
                '',
                Field('username', placeholder=self.fields['username'].label, autofocus=''),
                Field('password', placeholder=self.fields['password'].label),
            ),
            FormActions(Div(
                Div(
                    HTML(_(
                        '<a class="btn btn-link" href="{password_reset_url}">'
                        'Forgot Password?</a>'
                    ).format(password_reset_url=reverse('password_reset'))),
                    css_class='col-xs-6 m-t-2',
                ),
                Div(
                    Submit('save', _('Log In'), css_class='btn-lg btn-block'),
                    css_class='col-xs-6',
                ),
                css_class='row',
            ))
        )
        return helper


class PasswordResetForm(BasePasswordResetForm):

    email = forms.EmailField(label=_("Email Address"), max_length=254)

    @cached_property
    def helper(self):
        helper = FormHelper()
        helper.error_text_inline = False
        helper.label_class = 'sr-only'
        helper.attrs = {
            'autocomplete': 'off', 'autocorrect': 'off',
            'autocapitalize': 'off', 'spellcheck': 'false',
        }
        helper.layout = Layout(
            Fieldset(
                '',
                Field('email', placeholder=self.fields['email'].label),
            ),
            FormActions(Div(
                Div(
                    Submit(
                        'submit', _('Request Password Reset'),
                        css_class='btn btn-primary btn-block btn-lg'
                    ),
                    css_class='col-md-offset-1 col-md-10',
                ),
                css_class='nesting-form-group row'
            ))
        )
        return helper


class SetPasswordForm(BaseSetPasswordForm):
    @cached_property
    def helper(self):
        helper = FormHelper()
        helper.error_text_inline = False
        helper.label_class = 'sr-only'
        helper.attrs = {
            'autocomplete': 'off', 'autocorrect': 'off',
            'autocapitalize': 'off', 'spellcheck': 'false',
        }
        helper.layout = Layout(
            Fieldset(
                '',
                Field(
                    'new_password1',
                    placeholder=self.fields['new_password1'].label,
                ),
                Field(
                    'new_password2',
                    placeholder=self.fields['new_password2'].label,
                ),
            ),
            FormActions(Div(
                Div(
                    Submit(
                        'submit', _('Set Password'),
                        css_class='btn btn-primary btn-block btn-lg'
                    ),
                    css_class='col-md-offset-1 col-md-10',
                ),
                css_class='nesting-form-group row'
            ))
        )
        return helper


class CocAgreementForm(forms.Form):
    agree = forms.BooleanField(label=_('I agree to the code of conduct.'), required=False, widget=forms.CheckboxInput)

    def clean_agree(self):
        agree = self.cleaned_data["agree"]
        if not agree:
            raise forms.ValidationError(_('You must agree to continue.'))
