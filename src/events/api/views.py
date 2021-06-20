from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import views
from rest_framework.response import Response

from django.conf import settings

from events.models import ProposedTutorialEvent, SponsoredEvent, Schedule, KeynoteEvent
from proposals.models import TalkProposal, TutorialProposal

from . import serializers


class TalkDetailAPIView(RetrieveAPIView):

    queryset = TalkProposal.objects.all()
    serializer_class = serializers.TalkDetailSerializer


class TalkListAPIView(ListAPIView):

    queryset = TalkProposal.objects.filter_accepted()
    serializer_class = serializers.TalkListSerializer


class SponsoredEventListAPIView(ListAPIView):

    queryset = SponsoredEvent.objects.all()
    serializer_class = serializers.SponsoredEventSerializer


class TutorialDetailAPIView(RetrieveAPIView):

    queryset = ProposedTutorialEvent.objects.all()
    serializer_class = serializers.TutorialDetailSerializer


class TutorialListAPIView(views.APIView):
    def get(self, request):
        tutorial_data = TutorialProposal.objects.filter_accepted()

        response_data = {"tutorials": []}
        for tutorial in tutorial_data:
            response_data["tutorials"].append({
                "title": tutorial.title,
                "abstract": tutorial.abstract,
                "tutorial_id": tutorial.id
            })

        return Response(response_data)


class ScheduleAPIView(RetrieveAPIView):
    def get(self, request):
        queryset = Schedule.objects.all()

        response_data = {"schedule_html": [], "schedule_day": []}
        if queryset.exists():
            response_data["schedule_html"] = queryset.latest().html
        response_data["schedule_day"] = settings.EVENTS_DAY_NAMES.items()

        return Response(response_data)


class KeynoteEventListAPIView(views.APIView):
    def get(self, request):
        keynote_data = KeynoteEvent.objects.all()

        response_data = {"data": []}
        for keynote in keynote_data:
            response_data["data"].append({
                "speaker": {
                    "name_zh_hant":keynote.speaker_name_zh_hant,
                    "name_en_us": keynote.speaker_name_en_us,
                    "bio_zh_hant": keynote.speaker_bio_zh_hant,
                    "bio_en_us": keynote.speaker_bio_en_us,
                    # "photo": keynote.speaker_photo
                },
                "session":{
                    "title_zh_hant": keynote.session_title_zh_hant,
                    "title_en_us": keynote.session_title_en_us,
                    "description_zh_hant": keynote.session_description_zh_hant,
                    "description_en_us": keynote.session_description_en_us,
                    "slides": keynote.session_slides,
                },
                "slido": keynote.slido,
                "social_item": {
                    "linkedin": keynote.social_linkedin,
                    "twitter": keynote.social_twitter,
                    "github": keynote.social_github,
                }
            })
        return Response(response_data)
