from django.db.models import F
from django.http import JsonResponse
from django.views.generic.base import View
from django.views.generic import ListView

from core.utils import TemplateExistanceStatusResponse

from .models import Sponsor, OpenRole


class SponsorListView(ListView):

    model = Sponsor
    response_class = TemplateExistanceStatusResponse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SponsorAPIView(View):
    def get(self, request):
        sponsor_data = Sponsor.objects.order_by('level')

        level_dict = {}
        for sponsor in sponsor_data:
            if sponsor.level_en_name not in level_dict:
                level_dict[sponsor.level_en_name] = []

            level_dict[sponsor.level_en_name].append({
                "name": sponsor.name,
                "intro": sponsor.intro,
                "website_url": sponsor.website_url,
                "logo_url": sponsor.logo.url if sponsor.logo else ''
            })

        response_data = {"data": []}
        for level_name, sponsors in level_dict.items():
            response_data["data"].append({
                "level_name": level_name,
                "sponsors": sponsors
            })

        return JsonResponse(response_data)


class JobAPIView(View):
    def get(self, request):
        sponsor_has_open_role = set(OpenRole.objects.values_list('sponsor', flat=True))
        sponsor_set = Sponsor.objects.filter(id__in=sponsor_has_open_role).order_by('level')

        open_roles = OpenRole.objects.filter(sponsor__in=sponsor_has_open_role).order_by('sponsor__level')

        response_data = {"data": []}
        for sponsor in sponsor_set:
            jobs = []
            for open_role in open_roles:
                jobs.append({
                    "job_url": open_role.url,
                    "job_name": open_role.name,
                    "job_description": open_role.description,
                })
            response_data["data"].append({
                "sponsor_logo_url": sponsor.logo.url if sponsor.logo else '',
                "sponsor_name": sponsor.name,
                "jobs": jobs
            })

        return JsonResponse(response_data)
