from django.conf import settings
from rest_framework import views, status
from rest_framework.response import Response

from registry.helper import reg
from ext2020.models import Attendee


class AttendeeAPIView(views.APIView):
    model = Attendee

    def post(self, request):
        self.token = request.data['token']
        try:
            Attendee.objects.get(token=self.token)
            slug = settings.CONFERENCE_DEFAULT_SLUG
            key_filter = f"{slug}.live"
            num_rooms = [key for key in reg if key_filter in str(key)]

            response_data = {"youtube_infos": []}
            for idx, room in enumerate(num_rooms):
                response_data["youtube_infos"].append({
                    "room": f"R{idx+1}",
                    "video_id": reg.get(f'{room}', '')
                })
            return Response(response_data, status=status.HTTP_200_OK)
        except Attendee.DoesNotExist:
            response_data = {"status": "Attendee Dose Not Exist"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
