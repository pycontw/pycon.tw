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


class TalkDetailSerializer(serializers.ModelSerializer):
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


class TutorialDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    begin_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    python_level = serializers.SerializerMethodField()
    abstract = serializers.SerializerMethodField()
    detailed_description = serializers.SerializerMethodField()
    slide_link = serializers.SerializerMethodField()
    slido_embed_link = serializers.SerializerMethodField()
    speakers = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.proposal.title

    def get_date(self, obj):
        return obj.begin_time.value.strftime("%Y-%m-%d")

    def get_begin_time(self, obj):
        return obj.begin_time.value.strftime("%Y-%m-%d %H:%M:%S")

    def get_end_time(self, obj):
        return obj.end_time.value.strftime("%Y-%m-%d %H:%M:%S")

    def get_category(self, obj):
        return obj.proposal.category

    def get_language(self, obj):
        return obj.proposal.language

    def get_python_level(self, obj):
        return obj.proposal.python_level

    def get_abstract(self, obj):
        return obj.proposal.abstract

    def get_detailed_description(self, obj):
        return obj.proposal.detailed_description

    def get_slide_link(self, obj):
        return obj.proposal.slide_link

    def get_slido_embed_link(self, obj):
        return obj.proposal.slido_embed_link

    def get_speakers(self, obj):
        return [
            ReturnDict(PrimarySpeakerSerializer(
                data={'thumbnail_url': i.user.get_thumbnail_url(),
                      'name': i.user.speaker_name,
                      'github_profile_url': i.user.github_profile_url,
                      'twitter_profile_url': i.user.twitter_profile_url,
                      'facebook_profile_url': i.user.facebook_profile_url}).get_initial(),
                serializer=PrimarySpeakerSerializer) for i in obj.proposal.speakers]

    class Meta:
        model = models.ProposedTutorialEvent
        fields = [
            "title",
            "location",
            "date",
            "begin_time",
            "end_time",
            "category",
            "language",
            "python_level",
            "abstract",
            "detailed_description",
            "slide_link",
            "slido_embed_link",
            "speakers"
        ]
