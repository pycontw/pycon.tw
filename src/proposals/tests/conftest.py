import pytest

from proposals.models import AdditionalSpeaker, TutorialProposal


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
        title='Beyond the Style Guides<br>',
        language='ZHEN',
    )
    return proposal


@pytest.fixture
def cancelled_tutorial_proposal(tutorial_proposal):
    tutorial_proposal.cancelled = True
    tutorial_proposal.save()
    return tutorial_proposal


@pytest.fixture(params=['talk', 'tutorial'])
def proposal_type(request):
    return request.param


@pytest.fixture
def proposal(proposal_type, talk_proposal, tutorial_proposal):
    return locals()[proposal_type + '_proposal']


@pytest.fixture
def additional_speaker(another_user, proposal):
    speaker = AdditionalSpeaker.objects.create(
        id=81, user=another_user, proposal=proposal,
    )
    return speaker
