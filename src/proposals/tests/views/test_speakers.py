from core.utils import set_registry


def test_talk_proposal_manage_speakers_login(client):
    response = client.get(
        '/en-us/proposals/talk/42/manage-speakers/', follow=True,
    )
    assert response.redirect_chain == [
        ('/en-us/accounts/login/'
         '?next=/en-us/proposals/talk/42/manage-speakers/', 302),
    ]


def test_tutorial_proposal_manage_speakers_login(client):
    response = client.get(
        '/en-us/proposals/tutorial/42/manage-speakers/', follow=True,
    )
    assert response.redirect_chain == [
        ('/en-us/accounts/login/'
         '?next=/en-us/proposals/tutorial/42/manage-speakers/', 302),
    ]


def test_talk_proposal_manage_speakers_denied_get(bare_user_client):
    response = bare_user_client.get(
        '/en-us/proposals/talk/42/manage-speakers/',
    )
    assert response.status_code == 403


def test_tutorial_proposal_manage_speakers_denied_get(bare_user_client):
    response = bare_user_client.get(
        '/en-us/proposals/tutorial/42/manage-speakers/',
    )
    assert response.status_code == 403


def test_talk_proposal_manage_speakers_denied_post(bare_user_client):
    response = bare_user_client.post(
        '/en-us/proposals/talk/42/manage-speakers/',
    )
    assert response.status_code == 403


def test_tutorial_proposal_manage_speakers_denied_post(bare_user_client):
    response = bare_user_client.post(
        '/en-us/proposals/tutorial/42/manage-speakers/',
    )
    assert response.status_code == 403


def test_talk_proposal_manage_speakers_not_owned(
        another_user_client, talk_proposal):
    response = another_user_client.get(
        '/en-us/proposals/talk/42/manage-speakers/',
    )
    assert response.status_code == 404


def test_tutorial_proposal_manage_speakers_not_owned(
        another_user_client, tutorial_proposal):
    response = another_user_client.get(
        '/en-us/proposals/tutorial/42/manage-speakers/',
    )
    assert response.status_code == 404


def test_talk_proposal_manage_speakers_get_cancelled(
        user_client, cancelled_tutorial_proposal, parser):
    response = user_client.get('/en-us/proposals/tutorial/42/manage-speakers/')
    assert response.status_code == 404


def test_tutorial_proposal_manage_speakers_get_cancelled(
        user_client, cancelled_tutorial_proposal, parser):
    response = user_client.get('/en-us/proposals/tutorial/42/manage-speakers/')
    assert response.status_code == 404


@set_registry(**{'proposals.editable': True})
def test_talk_proposal_manage_speakers_get(user_client, talk_proposal):
    response = user_client.get('/en-us/proposals/talk/42/manage-speakers/')
    assert response.status_code == 200


@set_registry(**{'proposals.editable': True})
def test_tutorial_proposal_manage_speakers_get(
        user_client, tutorial_proposal):
    response = user_client.get('/en-us/proposals/tutorial/42/manage-speakers/')
    assert response.status_code == 200


@set_registry(**{'proposals.editable': True})
def test_talk_proposal_manage_speakers_post(
        user_client, talk_proposal, another_user):
    """Post to add an additional speaker. Redirect to self on success.
    """
    response = user_client.post(
        '/en-us/proposals/talk/42/manage-speakers/',
        {'email': another_user.email},
        follow=True,
    )
    assert response.redirect_chain == [
        ('/en-us/proposals/talk/42/manage-speakers/', 302),
    ]

    additional_speakers = talk_proposal.additionalspeaker_set.all()
    assert additional_speakers.count() == 1

    speaker = additional_speakers[0]
    assert speaker.user == another_user
    assert speaker.proposal == talk_proposal
    assert speaker.get_status_display() == 'Pending'


@set_registry(**{'proposals.editable': True})
def test_tutorial_proposal_manage_speakers_post(
        user_client, tutorial_proposal, another_user):
    """Post to add an additional speaker. Redirect to self on success.
    """
    response = user_client.post(
        '/en-us/proposals/tutorial/42/manage-speakers/',
        {'email': another_user.email},
        follow=True,
    )
    assert response.redirect_chain == [
        ('/en-us/proposals/tutorial/42/manage-speakers/', 302),
    ]

    additional_speakers = tutorial_proposal.additionalspeaker_set.all()
    assert additional_speakers.count() == 1

    speaker = additional_speakers[0]
    assert speaker.user == another_user
    assert speaker.proposal == tutorial_proposal
    assert speaker.get_status_display() == 'Pending'


@set_registry(**{'proposals.editable': True})
def test_remove_speaker_get_not_allowed(user_client, additional_speaker):
    response = user_client.get('/en-us/proposals/remove-speaker/81/')
    assert response.status_code == 405


@set_registry(**{'proposals.editable': True})
def test_remove_speaker_post_not_owned(
        another_user_client, additional_speaker):
    response = another_user_client.post(
        '/en-us/proposals/remove-speaker/81/',
        {'cancelled': 'true'},
    )
    assert response.status_code == 404


@set_registry(**{'proposals.editable': True})
def test_remove_speaker_post(user_client, proposal_type, additional_speaker):
    response = user_client.post(
        '/en-us/proposals/remove-speaker/81/',
        {'cancelled': 'true'},
        follow=True,
    )
    assert response.redirect_chain == [
        ('/en-us/proposals/{}/42/manage-speakers/'.format(proposal_type), 302),
    ]


@set_registry(**{'proposals.editable': True})
def test_set_speaker_status_get_not_allowed(
        another_user_client, additional_speaker):
    response = another_user_client.get(
        '/en-us/proposals/set-speaker-status/81/',
    )
    assert response.status_code == 405


@set_registry(**{'proposals.editable': True})
def test_set_speaker_status_post_not_owned(user_client, additional_speaker):
    response = user_client.post(
        '/en-us/proposals/set-speaker-status/81/',
        {'status': 'declined'},
    )
    assert response.status_code == 404


@set_registry(**{'proposals.editable': True})
def test_set_speaker_status_post(
        another_user_client, additional_speaker):
    response = another_user_client.post(
        '/en-us/proposals/set-speaker-status/81/',
        {'status': 'declined'},
        follow=True,
    )
    assert response.redirect_chain == [('/en-us/dashboard/', 302)]


@set_registry(**{'proposals.editable': False})
def test_talk_proposal_manage_speakers_get_disabled(user_client, talk_proposal):
    response = user_client.get('/en-us/proposals/talk/42/manage-speakers/')
    assert response.status_code == 404


@set_registry(**{'proposals.editable': False})
def test_tutorial_proposal_manage_speakers_get_disabled(
        user_client, tutorial_proposal):
    response = user_client.get('/en-us/proposals/tutorial/42/manage-speakers/')
    assert response.status_code == 404


@set_registry(**{'proposals.editable': False})
def test_talk_proposal_manage_speakers_post_disabled(
        user_client, talk_proposal, another_user):
    """Post to add an additional speaker. Redirect to self on success.
    """
    response = user_client.post(
        '/en-us/proposals/talk/42/manage-speakers/',
        {'email': another_user.email},
        follow=True,
    )

    assert response.status_code == 404


@set_registry(**{'proposals.editable': False})
def test_tutorial_proposal_manage_speakers_post_disabled(
        user_client, tutorial_proposal, another_user):
    """Post to add an additional speaker. Redirect to self on success.
    """
    response = user_client.post(
        '/en-us/proposals/tutorial/42/manage-speakers/',
        {'email': another_user.email},
        follow=True,
    )

    assert response.status_code == 404


@set_registry(**{'proposals.editable': False})
def test_remove_speaker_post_disabled(user_client, proposal_type, additional_speaker):
    response = user_client.post(
        '/en-us/proposals/remove-speaker/81/',
        {'cancelled': 'true'},
        follow=True,
    )

    assert response.status_code == 404


@set_registry(**{'proposals.editable': False})
def test_set_speaker_status_post_disabled(
        another_user_client, additional_speaker):
    response = another_user_client.post(
        '/en-us/proposals/set-speaker-status/81/',
        {'status': 'declined'},
        follow=True,
    )

    assert response.status_code == 404
