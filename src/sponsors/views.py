from django.views.generic import ListView

from .models import Sponsor


class SponsorListView(ListView):

    model = Sponsor
    ordering = 'level'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
