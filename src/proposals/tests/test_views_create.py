from django.contrib import messages
from proposals.models import TalkProposal, TutorialProposal


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


def test_tutorial_proposal_create_login(client):
    response = client.get('/proposals/tutorial/submit/', follow=True)
    assert response.redirect_chain == [
        ('/accounts/login/?next=/proposals/tutorial/submit/', 302),
    ]


def test_talk_proposal_create_denied_get(bare_user_client):
    response = bare_user_client.get('/proposals/talk/submit/')
    assert response.status_code == 403


def test_tutorial_proposal_create_denied_get(bare_user_client):
    response = bare_user_client.get('/proposals/tutorial/submit/')
    assert response.status_code == 403


def test_talk_proposal_create_denied_post(bare_user_client):
    response = bare_user_client.post('/proposals/talk/submit/')
    assert response.status_code == 403


def test_tutorial_proposal_create_denied_post(bare_user_client):
    response = bare_user_client.post('/proposals/tutorial/submit/')
    assert response.status_code == 403


def test_talk_proposal_create_get(user_client):
    response = user_client.get('/proposals/talk/submit/')
    assert response.status_code == 200


def test_tutorial_proposal_create_get(user_client):
    response = user_client.get('/proposals/tutorial/submit/')
    assert response.status_code == 200


def test_talk_proposal_create_post(user, user_client):
    response = user_client.post('/proposals/talk/submit/', {
        'title': 'Beyond the Style Guides<br>',
        'category': 'PRAC',
        'duration': 'PREF45',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    }, follow=True)

    proposal = TalkProposal.objects.get(
        submitter=user,
        title='Beyond the Style Guides<br>',
    )
    assert response.redirect_chain == [
        ('/proposals/talk/{pk}/edit/'.format(pk=proposal.pk), 302),
    ], response.context['form'].errors

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS,
         'Talk proposal '
         '<strong>Beyond the Style Guides&lt;br&gt;</strong> created.'),
    ]


def test_tutorial_proposal_create_post(user, user_client):
    response = user_client.post('/proposals/tutorial/submit/', {
        'title': 'Beyond the Style Guides<br>',
        'category': 'PRAC',
        'duration': 'FULLDAY',
        'language': 'CHI',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
    }, follow=True)

    proposal = TutorialProposal.objects.get(
        submitter=user,
        title='Beyond the Style Guides<br>',
    )
    assert response.redirect_chain == [
        ('/proposals/tutorial/{pk}/edit/'.format(pk=proposal.pk), 302),
    ], response.context['form'].errors

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS,
         'Tutorial proposal '
         '<strong>Beyond the Style Guides&lt;br&gt;</strong> created.'),
    ]
