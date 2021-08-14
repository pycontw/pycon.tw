from django.conf import settings
from rest_framework import views, status
from rest_framework.response import Response
from registry.helper import reg
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from attendee.models import Attendee


class AttendeeAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    model = Attendee

    def post(self, request):
        self.token = request.data['token']
        try:
            Attendee.objects.get(token=self.token)
            slug = settings.CONFERENCE_DEFAULT_SLUG
            key_prefix = f"{slug}.live"
            reg_room_keys = [
                key for key in reg if str(key).startswith(key_prefix)
            ]

            response_data = {"youtube_infos": []}
            for idx, room in enumerate(reg_room_keys):
                response_data["youtube_infos"].append({
                    "room": f"R{idx+1}",
                    "video_id": reg.get(f'{room}', '')
                })
            return Response(response_data, status=status.HTTP_200_OK)
        except Attendee.DoesNotExist:
            response_data = {"status": "Attendee Dose Not Exist"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
