from django.conf import settings
from registry.helper import reg
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from ext2020.models import Attendee


class AttendeeAPIView(views.APIView):
    model = Attendee

    def post(self, request):
        self.token = request.data['token']
        try:
            Attendee.objects.get(token=self.token)
            response_data = {"youtube_infos": []}
            for i in range(1, 4):
                response_data["youtube_infos"].append({
                    "room":
                    f"R{i}",
                    "video_id":
                    reg.get(f'{settings.CONFERENCE_DEFAULT_SLUG}.live.r{i}',
                            '')
                })
            return Response(response_data, status=status.HTTP_200_OK)
        except Attendee.DoesNotExist:
            response_data = {"status": "Attendee Dose Not Exist"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
