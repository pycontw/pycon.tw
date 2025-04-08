from rest_framework import serializers

from proposals.models import LLMReview, TalkProposal


class TalkProposalMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkProposal
        fields = ['id', 'title']


class LLMReviewSerializer(serializers.ModelSerializer):
    proposal = TalkProposalMinimalSerializer(read_only=True)
    proposal_id = serializers.PrimaryKeyRelatedField(
        queryset=TalkProposal.objects.all(),
        source='proposal',
        write_only=True
    )

    class Meta:
        model = LLMReview
        fields = [
            'id', 'proposal', 'proposal_id', 'summary', 'comment',
            'translated_summary', 'translated_comment', 'vote', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
