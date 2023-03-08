import pytest

from proposals.models import AdditionalSpeaker, TutorialProposal
from reviews.models import Review


@pytest.fixture
def cancelled_talk_proposal(talk_proposal):
    talk_proposal.cancelled = True
    talk_proposal.save()
    return talk_proposal


@pytest.fixture
def tutorial_proposal(user):
    proposal = TutorialProposal.objects.create(
        id=42,
        submitter=user,
        title="Beyond the Style Guides<br>",
        language="ZHEN",
    )
    return proposal


@pytest.fixture
def cancelled_tutorial_proposal(tutorial_proposal):
    tutorial_proposal.cancelled = True
    tutorial_proposal.save()
    return tutorial_proposal


@pytest.fixture(params=["talk", "tutorial"])
def proposal_type(request):
    return request.param


@pytest.fixture
def proposal(proposal_type, talk_proposal, tutorial_proposal):
    return locals()[proposal_type + "_proposal"]


@pytest.fixture
def additional_speaker(another_user, proposal):
    speaker = AdditionalSpeaker.objects.create(
        id=81,
        user=another_user,
        proposal=proposal,
    )
    return speaker


@pytest.fixture
def stage_1_review(user, another_user, talk_proposal):
    stage_1_review = [
        Review.objects.create(
            stage=1, reviewer=user, proposal=talk_proposal, vote="+1", comment="test"
        ),
        Review.objects.create(
            stage=1,
            reviewer=another_user,
            proposal=talk_proposal,
            vote="+1",
            comment="test",
        ),
    ]
    return stage_1_review


@pytest.fixture
def stage_2_review(user, talk_proposal):
    stage_2_review = [
        Review.objects.create(
            stage=2, reviewer=user, proposal=talk_proposal, vote="+1", comment="test"
        ),
    ]
    return stage_2_review
