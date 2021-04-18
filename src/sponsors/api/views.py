from rest_framework import views
from rest_framework.response import Response

from sponsors.models import Sponsor, OpenRole

class SponsorAPIView(views.APIView):
    def get(self, request):
        sponsor_data = Sponsor.objects.order_by('level')

        level_dict = {}
        for sponsor in sponsor_data:
            if sponsor.level_en_name not in level_dict:
                level_dict[sponsor.level_en_name] = []

            level_dict[sponsor.level_en_name].append({
                "name": sponsor.name,
                "subtitle_en_us": sponsor.subtitle_en_us,
                "subtitle_zh_hant": sponsor.subtitle_zh_hant,
                "intro_en_us": sponsor.intro_en_us,
                "intro_zh_hant": sponsor.intro_zh_hant,
                "website_url": sponsor.website_url,
                "logo_url": sponsor.logo.url if sponsor.logo else ''
            })

        response_data = {"data": []}
        for level_name, sponsors in level_dict.items():
            response_data["data"].append({
                "level_name": level_name,
                "sponsors": sponsors
            })

        return Response(response_data)


class JobAPIView(views.APIView):
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
                    "job_description_en_us": open_role.description_en_us,
                    "job_description_zh_hant": open_role.description_zh_hant,
                })
            response_data["data"].append({
                "sponsor_logo_url": sponsor.logo.url if sponsor.logo else '',
                "sponsor_name": sponsor.name,
                "jobs": jobs
            })

        return Response(response_data)
