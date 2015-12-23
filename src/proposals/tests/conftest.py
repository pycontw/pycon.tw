import pytest

from proposals.models import TalkProposal, TutorialProposal


@pytest.fixture
def talk_proposal(user):
    proposal = TalkProposal.objects.create(
        id=42,
        submitter=user,
        title='Beyond the Style Guides',
    )
    return proposal


@pytest.fixture
def tutorial_proposal(user):
    proposal = TutorialProposal.objects.create(
        id=42,
        submitter=user,
        title='Beyond the Style Guides',
    )
    return proposal
