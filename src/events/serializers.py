from rest_framework import serializers
from rest_framework.utils.serializer_helpers import (
    ReturnDict
)

from events import models


class PrimarySpeakerSerializer(serializers.Serializer):
    thumbnail_url = serializers.CharField()
    name = serializers.CharField()
    github_profile_url = serializers.CharField()
    twitter_profile_url = serializers.CharField()
    facebook_profile_url = serializers.CharField()


class TalkProposalListSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()

    def get_speakers(self, obj):
        return [
            ReturnDict(PrimarySpeakerSerializer(
                data={'thumbnail_url': i.user.get_thumbnail_url(),
                      'name': i.user.speaker_name,
                      'github_profile_url': i.user.github_profile_url,
                      'twitter_profile_url': i.user.twitter_profile_url,
                      'facebook_profile_url': i.user.facebook_profile_url}).get_initial(),
                       serializer=PrimarySpeakerSerializer) for i in obj.speakers]

    class Meta:
        model = models.TalkProposal
        fields = [
            "title",
            "category",
            "language",
            "python_level",
            "recording_policy",
            "abstract",
            "detailed_description",
            "slide_link",
            "slido_embed_link",
            # "sponsored"
            "speakers"

        ]
