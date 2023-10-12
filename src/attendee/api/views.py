from django.conf import settings
from registry.helper import reg
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from attendee.models import Attendee


class AttendeeAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    model = Attendee

    def post(self, request):
        self.token = request.data.get('token')
        try:
            Attendee.objects.get(token=self.token)
            key_prefix = f"{settings.CONFERENCE_DEFAULT_SLUG}.live."
            reg_live_infos = []
            for key in reg:
                if not str(key).startswith(key_prefix):
                    continue
                room_name = str(key)[len(key_prefix):]
                video_id = reg.get(key, '')
                reg_live_infos.append({
                    "room": room_name,
                    "video_id": video_id,
                })
            response_data = {"youtube_infos": sorted(reg_live_infos, key=lambda x: x.get("room"))}
            return Response(response_data, status=status.HTTP_200_OK)
        except Attendee.DoesNotExist:
            response_data = {"status": "Attendee Dose Not Exist"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
