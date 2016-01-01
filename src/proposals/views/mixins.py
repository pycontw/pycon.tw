from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class FormValidMessageMixin:

    form_valid_message_level = messages.SUCCESS
    form_valid_message = None

    def get_form_valid_message_level(self):
        return self.form_valid_message_level

    def get_form_valid_message(self):
        return self.form_valid_message

    def form_valid(self, form):
        response = super().form_valid(form)
        form_valid_message = self.get_form_valid_message()
        if form_valid_message:
            messages.add_message(
                self.request,
                self.get_form_valid_message_level(),
                form_valid_message,
            )
        return response


class UserProfileRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_anonymous() or not user.verified:
            raise PermissionDenied
        return True
