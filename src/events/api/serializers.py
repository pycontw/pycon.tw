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


def format_speakers_data(request, speakers, show_details=True):
    formatted = []
    for s in speakers:
        thumbnail_absolute_uri = request.build_absolute_uri(s.get_thumbnail_url())
        data = {
            'thumbnail_url': thumbnail_absolute_uri,
            'name': s.speaker_name,
        }
        if show_details:
            data = {
                **data,
                'bio': s.bio,
                'github_profile_url': s.github_profile_url,
                'twitter_profile_url': s.twitter_profile_url,
                'facebook_profile_url': s.facebook_profile_url,
            }
        serialized = PrimarySpeakerSerializer(data=data).get_initial()
        formatted.append(ReturnDict(serialized, serializer=PrimarySpeakerSerializer))
    return formatted


def flatten_proposal_field(representation, allow_fields=[]):
    """
    The helper function that used in `to_representation()` for
    flattening the `proposal` object from serialized
    `ProposedTalkEvent` or `ProposedTutorialEvent`.
    """
    proposal_repr = representation.pop('proposal')
    for key in proposal_repr:
        if key in allow_fields or not allow_fields:
            representation[key] = proposal_repr[key]
    return representation


class TalkProposalSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()
    event_type = serializers.ReadOnlyField(default='talk')

    def get_speakers(self, obj):
        request = self.context.get('request')
        speakers = [s.user for s in obj.speakers]
        return format_speakers_data(request, speakers)

    class Meta:
        model = TalkProposal
        fields = [
            "title", "category", "language", "python_level",
            "recording_policy", "abstract", "detailed_description",
            "slide_link", "slido_embed_link", "hackmd_embed_link",
            "speakers", "event_type",
        ]


class TalkDetailSerializer(serializers.ModelSerializer):
    proposal = TalkProposalSerializer()

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        return flatten_proposal_field(representation)

    class Meta:
        model = ProposedTalkEvent
        fields = [
            'id', 'proposal', 'begin_time', 'end_time', 'is_remote', 'location',
            'youtube_id',
        ]


class TalkListSerializer(serializers.ModelSerializer):
    proposal = TalkProposalSerializer()

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        allow_fields = ['title', 'category', 'speakers', 'event_type']
        return flatten_proposal_field(representation, allow_fields=allow_fields)

    class Meta:
        model = ProposedTalkEvent
        fields = ["id", "proposal"]


class SponsoredEventDetailSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()
    event_type = serializers.ReadOnlyField(default='sponsored')

    def get_speakers(self, obj):
        request = self.context.get('request')
        return format_speakers_data(request, [obj.host])

    def to_representation(self, obj):
        """
        Assign the value of `SponsoredEvent.remoting_policy` as `is_remote`
        """
        representation = super().to_representation(obj)
        is_remote = representation.pop('remoting_policy')
        representation['is_remote'] = is_remote
        return representation

    class Meta:
        model = SponsoredEvent
        fields = [
            "id", "title", "category", "language", "python_level",
            "recording_policy", "abstract", "detailed_description",
            "slide_link", "slido_embed_link", "hackmd_embed_link",
            "speakers", "location", "begin_time", "end_time",
            "remoting_policy", "event_type", 'youtube_id',
        ]


class SponsoredEventListSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()
    event_type = serializers.ReadOnlyField(default='sponsored')

    def get_speakers(self, obj):
        request = self.context.get('request')
        return format_speakers_data(request, [obj.host])

    class Meta:
        model = SponsoredEvent
        fields = ["id", "title", "category", "speakers", "event_type", ]


class TutorialProposalSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()
    event_type = serializers.ReadOnlyField(default='tutorial')

    def get_speakers(self, obj):
        request = self.context.get('request')
        speakers = [s.user for s in obj.speakers]
        return format_speakers_data(request, speakers)

    class Meta:
        model = TutorialProposal
        fields = [
            "title", "category", "language", "python_level",
            "recording_policy", "abstract", "detailed_description",
            "slide_link", "slido_embed_link", "hackmd_embed_link",
            "speakers", "event_type",
        ]


class TutorialDetailSerializer(serializers.ModelSerializer):
    proposal = TutorialProposalSerializer()

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        return flatten_proposal_field(representation)

    class Meta:
        model = ProposedTutorialEvent
        fields = [
            'id', 'proposal', 'begin_time', 'end_time', 'is_remote', 'location',
            'registration_link',
        ]


class TutorialListSerializer(serializers.ModelSerializer):
    proposal = TutorialProposalSerializer()

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        allow_fields = ['title', 'category', 'speakers', 'event_type']
        return flatten_proposal_field(representation, allow_fields=allow_fields)

    class Meta:
        model = ProposedTutorialEvent
        fields = ["id", "proposal"]


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
            "id",
            "speaker",
            "session",
            "slido",
            "hackmd_embed_link",
            "youtube_id",
            "social_item"
        ]
