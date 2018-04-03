from django.views.generic import ListView

from core.utils import TemplateExistanceStatusResponse

from .models import Sponsor


class SponsorListView(ListView):

    model = Sponsor
    response_class = TemplateExistanceStatusResponse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
