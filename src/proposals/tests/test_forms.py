from django.contrib.auth.models import AnonymousUser

from proposals.forms import (
    TalkProposalCreateForm, TalkProposalUpdateForm,
    TutorialProposalCreateForm, TutorialProposalUpdateForm,
)


def test_talk_proposal_create_form():
    form = TalkProposalCreateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language',
        'python_level', 'recording_policy',
    ]


def test_talk_proposal_create_form_no_request():
    form = TalkProposalCreateForm(data={
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'PREF45',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    })
    assert not form.is_valid()
    assert form.errors == {
        '__all__': ['Proposal creation requires a request object.'],
    }


def test_talk_proposal_create_form_anonymous(request):
    request.user = AnonymousUser()
    form = TalkProposalCreateForm(request=request, data={
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'PREF45',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    })
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'Only authenticated user with complete speaker profile may '
            'submit a proposal.',
        ],
    }


def test_talk_proposal_create_form_no_profile(request, bare_user):
    request.user = bare_user
    form = TalkProposalCreateForm(request=request, data={
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'PREF45',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    })
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'Only authenticated user with complete speaker profile may '
            'submit a proposal.',
        ],
    }


def test_talk_proposal_create_form_valid(request, user):
    request.user = user
    form = TalkProposalCreateForm(request=request, data={
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'PREF45',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    })
    assert form.is_valid()


def test_tutorial_proposal_create_form():
    form = TutorialProposalCreateForm()
    assert list(form.fields) == [
        'title', 'category', 'duration', 'language',
        'python_level', 'recording_policy',
    ]


def test_tutorial_proposal_create_form_no_request():
    form = TutorialProposalCreateForm(data={
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'HALFDAY',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    })
    assert not form.is_valid()
    assert form.errors == {
        '__all__': ['Proposal creation requires a request object.'],
    }


def test_tutorial_proposal_create_form_anonymous(request):
    request.user = AnonymousUser()
    form = TutorialProposalCreateForm(request=request, data={
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'HALFDAY',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    })
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'Only authenticated user with complete speaker profile may '
            'submit a proposal.',
        ],
    }


def test_tutorial_proposal_create_form_no_profile(request, bare_user):
    request.user = bare_user
    form = TutorialProposalCreateForm(request=request, data={
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'HALFDAY',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    })
    assert not form.is_valid()
    assert form.errors == {
        '__all__': [
            'Only authenticated user with complete speaker profile may '
            'submit a proposal.',
        ],
    }


def test_tutorial_proposal_create_form_valid(request, user):
    request.user = user
    form = TutorialProposalCreateForm(request=request, data={
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'HALFDAY',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    })
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
