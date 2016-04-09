from django.views.generic import ListView

from .models import Sponsor


class SponsorListView(ListView):

    model = Sponsor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platinum_sponsors'] = Sponsor.objects.filter(
            level=Sponsor.Level.PLATINUM
        )
        context['gold_sponsors'] = Sponsor.objects.filter(
            level=Sponsor.Level.GOLD
        )
        context['silver_sponsors'] = Sponsor.objects.filter(
            level=Sponsor.Level.SILVER
        )
        context['bronze_sponsors'] = Sponsor.objects.filter(
            level=Sponsor.Level.BRONZE
        )
        context['special_sponsors'] = Sponsor.objects.filter(
            level=Sponsor.Level.SPECIAL
        )
        return context
