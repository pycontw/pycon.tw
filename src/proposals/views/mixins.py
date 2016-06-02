from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404


class UserProfileRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_anonymous() or not user.verified:
            raise PermissionDenied
        return True


class ProposalEditMixin:

    def can_edit(self):
        return settings.PROPOSALS_EDITABLE

    def dispatch(self, request, *args, **kwargs):
        if not self.can_edit():
            raise Http404
        return super().dispatch(request, *args, **kwargs)
