import pytest

from django.contrib import messages
from django.contrib.auth import get_user_model

from proposals.models import Proposal


User = get_user_model()


@pytest.fixture
def another_user(db):
    try:
        user = User.objects.get(email='another@ayatsuji.itou')
    except User.DoesNotExist:
        user = User.objects.create_user(
            email='another@ayatsuji.itou',
            password='7uk1T0n01sY',
            speaker_name='Misaki Mei',
            bio='Neon marketing office assault kanji into meta-face.',
        )
    assert user.profile_filled
    return user


@pytest.fixture
def another_user_client(another_user, client):
    client.login(email='another@ayatsuji.itou', password='7uk1T0n01sY')
    return client


@pytest.fixture
def proposal(user):
    proposal = Proposal.objects.create(
        id=42,
        submitter=user,
        title='Beyond the Style Guides',
    )
    return proposal


def test_proposal_create_login(client):
    response = client.get('/proposals/submit/', follow=True)
    assert response.redirect_chain == [
        ('http://testserver/accounts/login/?next=/proposals/submit/', 302),
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


def test_proposal_create_post(user, user_client):
    response = user_client.post('/proposals/submit/', {
        'title': 'Beyond the Style Guides',
        'category': 'PRAC',
        'duration': 'PREF45',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    }, follow=True)

    proposal = user.proposal_set.get(title='Beyond the Style Guides')
    assert response.redirect_chain == [
        ('http://testserver/proposals/{pk}/edit/'.format(pk=proposal.pk), 302),
    ]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [(messages.SUCCESS, 'Proposal created.')]


def test_proposal_edit_login(client):
    response = client.get('/proposals/42/edit/', follow=True)
    assert response.redirect_chain == [
        ('http://testserver/accounts/login/?next=/proposals/42/edit/', 302),
    ]


def test_proposal_edit_denied_get(bare_user_client):
    response = bare_user_client.get('/proposals/42/edit/')
    assert response.status_code == 403


def test_proposal_edit_denied_post(bare_user_client):
    response = bare_user_client.post('/proposals/42/edit/')
    assert response.status_code == 403


def test_proposal_edit_not_owned(another_user_client, proposal):
    response = another_user_client.get('/proposals/42/edit/')
    assert response.status_code == 404


def test_proposal_edit_get(user_client, proposal):
    response = user_client.get('/proposals/42/edit/')
    assert response.status_code == 200


def test_proposal_edit_post(user_client, proposal):
    response = user_client.post('/proposals/42/edit/', {
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
            "enough?\n\n"
            "The answer is “No”. To write maintainable code, you need more "
            "than the style guides. In this share, I will introduce you the "
            "keys of writing high maintainability code.\n\n"
        ),
        'objectives': (
            "You will be able to write better code after this talk. Save both "
            "you and your co-workers’ time from hating each other, and build "
            "more exciting feature together. :)"
        ),
        'detailed_description': 'Time is money. — Benjamin Franklin',
    }, follow=True)

    assert response.redirect_chain == [('http://testserver/dashboard/', 302)]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [(messages.SUCCESS, 'Proposal updated.')]
