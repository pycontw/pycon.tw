import pytest

from django.contrib import messages
from django.contrib.auth import get_user_model

from proposals.models import TalkProposal, TutorialProposal


User = get_user_model()


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


def test_proposal_create_login(client):
    response = client.get('/proposals/submit/', follow=True)
    assert response.redirect_chain == [
        ('/accounts/login/?next=/proposals/submit/', 302),
    ]


def test_proposal_create_denied_get(bare_user_client):
    response = bare_user_client.get('/proposals/submit/')
    assert response.status_code == 403


def test_proposal_create_denied_post(bare_user_client):
    response = bare_user_client.post('/proposals/submit/')
    assert response.status_code == 403


def test_proposal_create_get(user_client):
    response = user_client.get('/proposals/submit/')
    assert response.status_code == 200


def test_talk_proposal_create_login(client):
    response = client.get('/proposals/talk/submit/', follow=True)
    assert response.redirect_chain == [
        ('/accounts/login/?next=/proposals/talk/submit/', 302),
    ]


def test_talk_proposal_create_denied_get(bare_user_client):
    response = bare_user_client.get('/proposals/talk/submit/')
    assert response.status_code == 403


def test_talk_proposal_create_denied_post(bare_user_client):
    response = bare_user_client.post('/proposals/talk/submit/')
    assert response.status_code == 403


def test_talk_proposal_create_get(user_client):
    response = user_client.get('/proposals/talk/submit/')
    assert response.status_code == 200


def test_talk_proposal_create_post(user, user_client):
    response = user_client.post('/proposals/talk/submit/', {
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'PREF45',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    }, follow=True)

    proposal = TalkProposal.objects.get(
        submitter=user,
        title='Beyond the Style Guides',
    )
    assert response.redirect_chain == [
        ('/proposals/talk/{pk}/edit/'.format(pk=proposal.pk), 302),
    ]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [(messages.SUCCESS, 'Talk proposal created.')]


def test_talk_proposal_edit_login(client):
    response = client.get('/proposals/talk/42/edit/', follow=True)
    assert response.redirect_chain == [
        ('/accounts/login/?next=/proposals/talk/42/edit/', 302),
    ]


def test_talk_proposal_edit_denied_get(bare_user_client):
    response = bare_user_client.get('/proposals/talk/42/edit/')
    assert response.status_code == 403


def test_talk_proposal_edit_denied_post(bare_user_client):
    response = bare_user_client.post('/proposals/talk/42/edit/')
    assert response.status_code == 403


def test_talk_proposal_edit_not_owned(another_user_client, talk_proposal):
    response = another_user_client.get('/proposals/talk/42/edit/')
    assert response.status_code == 404


def test_talk_proposal_edit_get(user_client, talk_proposal):
    response = user_client.get('/proposals/talk/42/edit/')
    assert response.status_code == 200


def test_talk_proposal_edit_post(user_client, talk_proposal):
    response = user_client.post('/proposals/talk/42/edit/', {
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'PREF45',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
        'target_audience': (
            'Who can program, but wants to write more beautiful code.'
        ),
        'abstract': (
            "In the modern world, programmer’s time is more expensive than "
            "computer’s time. Better maintainability saves more. To improve "
            "it, you may be following “______ Style Guide”. But is it "
            "enough?"
        ),
        'objective': (
            "People can write more maintainable code and get happier."
        ),
        'detailed_description': (
            "The answer is “No”. To write maintainable code, you need more "
            "than the style guides. In this share, I will introduce you the "
            "keys of writing high maintainability code."
        ),
        'outline': (
            "You will be able to write better code after this talk. Save both "
            "you and your co-workers’ time from hating each other, and build "
            "more exciting feature together. :)"
        ),
    }, follow=True)

    assert response.redirect_chain == [('/dashboard/', 302)]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [(messages.SUCCESS, 'Talk proposal updated.')]


def test_tutorial_proposal_create_login(client):
    response = client.get('/proposals/tutorial/submit/', follow=True)
    assert response.redirect_chain == [
        ('/accounts/login/?next=/proposals/tutorial/submit/', 302),
    ]


def test_tutorial_proposal_create_denied_get(bare_user_client):
    response = bare_user_client.get('/proposals/tutorial/submit/')
    assert response.status_code == 403


def test_tutorial_proposal_create_denied_post(bare_user_client):
    response = bare_user_client.post('/proposals/tutorial/submit/')
    assert response.status_code == 403


def test_tutorial_proposal_create_get(user_client):
    response = user_client.get('/proposals/tutorial/submit/')
    assert response.status_code == 200


def test_tutorial_proposal_create_post(user, user_client):
    response = user_client.post('/proposals/tutorial/submit/', {
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    }, follow=True)

    proposal = TutorialProposal.objects.get(
        submitter=user,
        title='Beyond the Style Guides',
    )
    assert response.redirect_chain == [
        ('/proposals/tutorial/{pk}/edit/'.format(pk=proposal.pk), 302),
    ]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [(messages.SUCCESS, 'Tutorial proposal created.')]


def test_tutorial_proposal_edit_login(client):
    response = client.get('/proposals/tutorial/42/edit/', follow=True)
    assert response.redirect_chain == [
        ('/accounts/login/?next=/proposals/tutorial/42/edit/', 302),
    ]


def test_tutorial_proposal_edit_denied_get(bare_user_client):
    response = bare_user_client.get('/proposals/tutorial/42/edit/')
    assert response.status_code == 403


def test_tutorial_proposal_edit_denied_post(bare_user_client):
    response = bare_user_client.post('/proposals/tutorial/42/edit/')
    assert response.status_code == 403


def test_tutorial_proposal_edit_not_owned(
        another_user_client, tutorial_proposal):
    response = another_user_client.get('/proposals/tutorial/42/edit/')
    assert response.status_code == 404


def test_tutorial_proposal_edit_get(user_client, tutorial_proposal):
    response = user_client.get('/proposals/tutorial/42/edit/')
    assert response.status_code == 200


def test_tutorial_proposal_edit_post(user_client, tutorial_proposal):
    response = user_client.post('/proposals/tutorial/42/edit/', {
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
        'target_audience': (
            'Who can program, but wants to write more beautiful code.'
        ),
        'abstract': (
            "In the modern world, programmer’s time is more expensive than "
            "computer’s time. Better maintainability saves more. To improve "
            "it, you may be following “______ Style Guide”. But is it "
            "enough?"
        ),
        'objective': (
            "People can write more maintainable code and get happier."
        ),
        'detailed_description': (
            "The answer is “No”. To write maintainable code, you need more "
            "than the style guides. In this share, I will introduce you the "
            "keys of writing high maintainability code."
        ),
        'outline': (
            "You will be able to write better code after this talk. Save both "
            "you and your co-workers’ time from hating each other, and build "
            "more exciting feature together. :)"
        ),
    }, follow=True)

    assert response.redirect_chain == [('/dashboard/', 302)]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [(messages.SUCCESS, 'Tutorial proposal updated.')]
