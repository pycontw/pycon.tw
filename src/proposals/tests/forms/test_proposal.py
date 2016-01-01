import pytest

from proposals.forms import (
    TalkProposalCreateForm, TalkProposalUpdateForm,
    TutorialProposalCreateForm, TutorialProposalUpdateForm,
)


@pytest.fixture
def talk_proposal_data():
    return {
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'PREF45',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    }


def test_talk_proposal_create_form():
    form = TalkProposalCreateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language',
        'python_level', 'recording_policy',
    ]


def test_talk_proposal_create_form_no_request(talk_proposal_data):
    form = TalkProposalCreateForm(data=talk_proposal_data)
    assert not form.is_valid()
    assert form.errors == {
        '__all__': ['Talk proposal creation requires a request object.'],
    }


def test_talk_proposal_create_form_invalid_user(
        talk_proposal_data, request, invalid_user):
    request.user = invalid_user
    form = TalkProposalCreateForm(request=request, data=talk_proposal_data)
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'Only authenticated user with complete speaker profile may '
            'create a talk proposal.',
        ],
    }


def test_talk_proposal_create_form_valid(talk_proposal_data, request, user):
    request.user = user
    form = TalkProposalCreateForm(request=request, data=talk_proposal_data)
    assert form.is_valid()


@pytest.fixture
def tutorial_proposal_data():
    return {
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'HALFDAY',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    }


def test_tutorial_proposal_create_form():
    form = TutorialProposalCreateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language',
        'python_level', 'recording_policy',
    ]


def test_tutorial_proposal_create_form_no_request(tutorial_proposal_data):
    form = TutorialProposalCreateForm(data=tutorial_proposal_data)
    assert not form.is_valid()
    assert form.errors == {
        '__all__': ['Tutorial proposal creation requires a request object.'],
    }


def test_tutorial_proposal_create_form_anonymous(
        tutorial_proposal_data, request, invalid_user):
    request.user = invalid_user
    form = TutorialProposalCreateForm(
        request=request, data=tutorial_proposal_data,
    )
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'Only authenticated user with complete speaker profile may '
            'create a tutorial proposal.',
        ],
    }


def test_tutorial_proposal_create_form_valid(
        tutorial_proposal_data, request, user):
    request.user = user
    form = TutorialProposalCreateForm(
        request=request, data=tutorial_proposal_data,
    )
    assert form.is_valid()


def test_talk_proposal_update_form():
    form = TalkProposalUpdateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language', 'target_audience',
        'abstract', 'python_level', 'objective', 'detailed_description',
        'outline', 'supplementary', 'recording_policy', 'slide_link',
    ]


def test_tutorial_proposal_update_form():
    form = TutorialProposalUpdateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language', 'target_audience',
        'abstract', 'python_level', 'objective', 'detailed_description',
        'outline', 'supplementary', 'recording_policy', 'slide_link',
    ]
