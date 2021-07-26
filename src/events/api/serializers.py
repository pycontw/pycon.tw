from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from events.models import ProposedTalkEvent, ProposedTutorialEvent, SponsoredEvent, KeynoteEvent
from proposals.models import TalkProposal, TutorialProposal


class PrimarySpeakerSerializer(serializers.Serializer):
    thumbnail_url = serializers.CharField()
    name = serializers.CharField()
    github_profile_url = serializers.CharField()
    twitter_profile_url = serializers.CharField()
    facebook_profile_url = serializers.CharField()
    bio = serializers.CharField()


def format_speakers_data(request, speakers, show_details=False):
    formatted = []
    for speaker in speakers:
        u = speaker.user
        thumbnail_absolute_uri = request.build_absolute_uri(u.get_thumbnail_url())
        data = {
            'thumbnail_url': thumbnail_absolute_uri,
            'name': u.speaker_name,
        }
        if show_details:
            data = {
                **data,
                'bio': u.bio,
                'github_profile_url': u.github_profile_url,
                'twitter_profile_url': u.twitter_profile_url,
                'facebook_profile_url': u.facebook_profile_url,
            }
        serialized = PrimarySpeakerSerializer(data=data).get_initial()
        formatted.append(ReturnDict(serialized, serializer=PrimarySpeakerSerializer))
    return formatted


class TalkProposalSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()

    def get_speakers(self, obj):
        request = self.context.get('request')
        return format_speakers_data(request, obj.speakers, show_details=True)

    class Meta:
        model = TalkProposal
        fields = [
            "title", "category", "language", "python_level",
            "recording_policy", "abstract", "detailed_description",
            "slide_link", "slido_embed_link", "speakers",
            # "sponsored"
        ]


class TalkDetailSerializer(serializers.ModelSerializer):
    proposal = TalkProposalSerializer()

    class Meta:
        model = ProposedTalkEvent
        fields = ['proposal', 'begin_time', 'end_time', 'is_remote', 'location']


class TalkListSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()

    def get_speakers(self, obj):
        request = self.context.get('request')
        return format_speakers_data(request, obj.speakers)

    class Meta:
        model = TalkProposal
        fields = ["id", "title", "category", "speakers"]


class SponsoredEventSerializer(serializers.ModelSerializer):

    host_name = serializers.CharField(source="host.speaker_name", required=False)

    class Meta:
        model = SponsoredEvent
        fields = ["slug", "title", "host_name"]


class TutorialProposalSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()

    def get_speakers(self, obj):
        request = self.context.get('request')
        return format_speakers_data(request, obj.speakers, show_details=True)

    class Meta:
        model = TutorialProposal
        fields = [
            "title", "category", "language", "python_level",
            "recording_policy", "abstract", "detailed_description",
            "slide_link", "slido_embed_link", "speakers",
        ]


class TutorialDetailSerializer(serializers.ModelSerializer):
    proposal = TutorialProposalSerializer()

    class Meta:
        model = ProposedTutorialEvent
        fields = ['proposal', 'begin_time', 'end_time', 'is_remote', 'location']


class TutorialListSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()

    def get_speakers(self, obj):
        request = self.context.get('request')
        return format_speakers_data(request, obj.speakers)

    class Meta:
        model = TutorialProposal
        fields = ["id", "title", "category", "speakers"]


class KeynoteEventSerializer(serializers.ModelSerializer):
    speaker = serializers.SerializerMethodField()
    session = serializers.SerializerMethodField()
    social_item = serializers.SerializerMethodField()

    def get_speaker(self, obj):
        return {
            "name_zh_hant": obj.speaker_name_zh_hant,
            "name_en_us": obj.speaker_name_en_us,
            "bio_zh_hant": obj.speaker_bio_zh_hant,
            "bio_en_us": obj.speaker_bio_en_us,
            "photo": obj.speaker_photo.url,
        }

    def get_session(self, obj):
        return {
            "title_zh_hant": obj.session_title_zh_hant,
            "title_en_us": obj.session_title_en_us,
            "description_zh_hant": obj.session_description_zh_hant,
            "description_en_us": obj.session_description_en_us,
            "slides": obj.session_slides,
        }

    def get_social_item(self, obj):
        return {
            "linkedin": obj.social_linkedin,
            "twitter": obj.social_twitter,
            "github": obj.social_github,
        }

    class Meta:
        model = KeynoteEvent
        fields = [
            "speaker",
            "session",
            "slido",
            "youtube_id",
            "social_item"
        ]
