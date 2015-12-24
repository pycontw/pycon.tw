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
def cancelled_talk_proposal(talk_proposal):
    talk_proposal.cancelled = True
    talk_proposal.save()
    return talk_proposal


@pytest.fixture
def tutorial_proposal(user):
    proposal = TutorialProposal.objects.create(
        id=42,
        submitter=user,
        title='Beyond the Style Guides',
    )
    return proposal


@pytest.fixture
def cancelled_tutorial_proposal(tutorial_proposal):
    tutorial_proposal.cancelled = True
    tutorial_proposal.save()
    return tutorial_proposal
