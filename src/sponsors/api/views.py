from collections import OrderedDict

from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.authentication import TokenAuthentication
from sponsors.models import Sponsor, OpenRole


class SponsorAPIView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
        open_roles = OpenRole.objects.all().order_by('sponsor__level')

        data = OrderedDict()
        for open_role in open_roles:
            sponsor_id = open_role.sponsor.id
            if sponsor_id not in data:
                logo = open_role.sponsor.logo
                data[sponsor_id] = {
                    "sponsor_logo_url": logo.url if logo else '',
                    "sponsor_name": open_role.sponsor.name,
                    "jobs": [],
                }
            data[sponsor_id]["jobs"].append({
                "job_url": open_role.url,
                "job_name_en_us": open_role.name_en_us,
                "job_name_zh_hant": open_role.name_zh_hant,
                "job_description_en_us": open_role.description_en_us,
                "job_description_zh_hant": open_role.description_zh_hant,
                "job_requirements_en_us": open_role.requirements_en_us,
                "job_requirements_zh_hant": open_role.requirements_zh_hant,
            })

        response_data = {"data": list(data.values())}
        return Response(response_data)
