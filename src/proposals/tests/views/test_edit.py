import pytest

from django.conf import settings
from django.contrib import messages

from core.utils import set_registry


def test_talk_proposal_edit_login(client):
    response = client.get('/en-us/proposals/talk/42/edit/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/login/?next=/en-us/proposals/talk/42/edit/', 302),
    ]


def test_tutorial_proposal_edit_login(client):
    response = client.get('/en-us/proposals/tutorial/42/edit/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/login/?next=/en-us/proposals/tutorial/42/edit/',
         302),
    ]


@set_registry(**{'proposals.editable': True})
def test_talk_proposal_edit_denied_get(bare_user_client):
    response = bare_user_client.get('/en-us/proposals/talk/42/edit/')
    assert response.status_code == 403


@set_registry(**{'proposals.editable': True})
def test_tutorial_proposal_edit_denied_get(bare_user_client):
    response = bare_user_client.get('/en-us/proposals/tutorial/42/edit/')
    assert response.status_code == 403


@set_registry(**{'proposals.editable': True})
def test_talk_proposal_edit_denied_post(bare_user_client):
    response = bare_user_client.post('/en-us/proposals/talk/42/edit/')
    assert response.status_code == 403


@set_registry(**{'proposals.editable': True})
def test_tutorial_proposal_edit_denied_post(bare_user_client):
    response = bare_user_client.post('/en-us/proposals/tutorial/42/edit/')
    assert response.status_code == 403


@set_registry(**{'proposals.editable': False})
def test_talk_proposal_edit_disabled_get(agreed_user_client, talk_proposal):
    response = agreed_user_client.get('/en-us/proposals/talk/42/edit/')
    assert response.status_code == 404


@set_registry(**{'proposals.editable': False})
def test_tutorial_proposal_edit_disabled_get(agreed_user_client, tutorial_proposal):
    response = agreed_user_client.get('/en-us/proposals/tutorial/42/edit/')
    assert response.status_code == 404


@set_registry(**{'proposals.editable': False})
def test_talk_proposal_edit_disabled_post(agreed_user_client, talk_proposal):
    response = agreed_user_client.post('/en-us/proposals/talk/42/edit/')
    assert response.status_code == 404


@set_registry(**{'proposals.editable': False})
def test_tutorial_proposal_edit_disabled_post(agreed_user_client, tutorial_proposal):
    response = agreed_user_client.post('/en-us/proposals/tutorial/42/edit/')
    assert response.status_code == 404


# yychen(2020-02-24): I think coc agreement check should come after owner check
# But I have no idea how to do it
# So this is just a workaround
@set_registry(**{'proposals.editable': True})
def test_talk_proposal_edit_not_owned(another_agreed_user_client, talk_proposal):
    response = another_agreed_user_client.get('/en-us/proposals/talk/42/edit/')
    assert response.status_code == 404


@set_registry(**{'proposals.editable': True})
def test_tutorial_proposal_edit_not_owned(
        another_agreed_user_client, tutorial_proposal):
    response = another_agreed_user_client.get('/en-us/proposals/tutorial/42/edit/')
    assert response.status_code == 404


@set_registry(**{'proposals.editable': True})
def test_talk_proposal_edit_get(agreed_user_client, talk_proposal):
    response = agreed_user_client.get('/en-us/proposals/talk/42/edit/')
    assert response.status_code == 200


@pytest.mark.xfail(strict=True, reason='TODO: why is this xfail?')
@set_registry(**{'proposals.editable': True})
def test_talk_proposal_edit_get_ui(user_client, talk_proposal, parser):
    body = parser.parse(user_client.get('/en-us/proposals/talk/42/edit/'))
    submit_buttons = body.cssselect(    # Except form inside navbar.
        'form:not(.navbar-form) button[type="submit"]'
    )
    assert len(submit_buttons) == 2

    form_element = next(submit_buttons[0].iterancestors('form'))
    assert not form_element.get('action')   # Posts to the same view.

    assert submit_buttons[1].get('name') == 'cancelled'
    assert submit_buttons[1].get('value')   # Should evaluate to True

    form_element = next(submit_buttons[1].iterancestors('form'))
    assert form_element.get('action') == '/proposals/talk/42/cancel/'


@set_registry(**{'proposals.editable': True})
def test_talk_proposal_edit_get_cancelled_ui(
        agreed_user_client, cancelled_talk_proposal, parser):
    """If a proposal is cancelled, the edit view should have only one form to
    re-activate it.
    """
    body = parser.parse(agreed_user_client.get('/en-us/proposals/talk/42/edit/'))
    submit_buttons = body.cssselect(    # Except form inside navbar.
        'form:not(.navbar-form) button[type="submit"]'
    )
    assert len(submit_buttons) == 1

    form_element = next(submit_buttons[0].iterancestors('form'))
    assert not form_element.get('action')   # Posts to the same view.


@set_registry(**{'proposals.editable': True})
def test_tutorial_proposal_edit_get(agreed_user_client, tutorial_proposal):
    response = agreed_user_client.get('/en-us/proposals/tutorial/42/edit/')
    assert response.status_code == 200


@pytest.mark.xfail(strict=True, reason='TODO: why is this xfail?')
@set_registry(**{'proposals.editable': True})
def test_tutorial_proposal_edit_get_ui(user_client, tutorial_proposal, parser):
    body = parser.parse(user_client.get('/en-us/proposals/tutorial/42/edit/'))
    submit_buttons = body.cssselect(    # Except form inside navbar.
        'form:not(.navbar-form) button[type="submit"]'
    )
    assert len(submit_buttons) == 2

    form_element = next(submit_buttons[0].iterancestors('form'))
    assert not form_element.get('action')   # Posts to the same view.

    assert submit_buttons[1].get('name') == 'cancelled'
    assert submit_buttons[1].get('value')   # Should evaluate to True

    form_element = next(submit_buttons[1].iterancestors('form'))
    assert form_element.get('action') == '/en-us/proposals/tutorial/42/cancel/'


@set_registry(**{'proposals.editable': True})
def test_tutorial_proposal_edit_get_cancelled(
        agreed_user_client, cancelled_tutorial_proposal, parser):
    """If a proposal is cancelled, the edit view should have only one form to
    re-activate it.
    """
    body = parser.parse(agreed_user_client.get('/en-us/proposals/tutorial/42/edit/'))
    submit_buttons = body.cssselect(    # Except form inside navbar.
        'form:not(.navbar-form) button[type="submit"]'
    )
    assert len(submit_buttons) == 1

    form_element = next(submit_buttons[0].iterancestors('form'))
    assert not form_element.get('action')   # Posts to the same view.


@set_registry(**{'proposals.editable': True})
def test_talk_proposal_edit_post(agreed_user_client, talk_proposal):
    response = agreed_user_client.post('/en-us/proposals/talk/42/edit/', {
        'title': 'Beyond the Style Guides<br>',
        'category': 'PRAC',
        'duration': 'PREF15',
        'language': 'ZHZH',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
        'referring_policy': False,
        'remoting_policy': True,
        'first_time_speaker': True,
        'abstract': (
            "In the modern world, programmer’s time is more expensive than "
            "computer’s time. Better maintainability saves more. To improve "
            "it, you may be following “______ Style Guide”. But is it "
            "enough?"
        ),
        'objective': (
            "Aim for those who can code, but wants to write more beautiful "
            "code. People can write more maintainable code and get happier."
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

    assert response.redirect_chain == [('/en-us/dashboard/', 302)], (
        response.context['form'].errors
    )

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS,
         'Talk proposal '
         '<strong>Beyond the Style Guides&lt;br&gt;</strong> updated.'),
    ]


@set_registry(**{'proposals.editable': True})
def test_tutorial_proposal_edit_post(agreed_user_client, tutorial_proposal):
    response = agreed_user_client.post('/en-us/proposals/tutorial/42/edit/', {
        'title': 'Beyond the Style Guides<br>',
        'category': 'PRAC',
        'duration': 'FULLDAY',
        'language': 'ZHZH',
        'python_level': 'INTERMEDIATE',
        'recording_policy': True,
        'remoting_policy': True,
        'abstract': (
            "In the modern world, programmer’s time is more expensive than "
            "computer’s time. Better maintainability saves more. To improve "
            "it, you may be following “______ Style Guide”. But is it "
            "enough?"
        ),
        'objective': (
            "Aim for those who can code, but wants to write more beautiful "
            "code. People can write more maintainable code and get happier."
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

    assert response.redirect_chain == [('/en-us/dashboard/', 302)], (
        response.context['form'].errors
    )

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS,
         'Tutorial proposal '
         '<strong>Beyond the Style Guides&lt;br&gt;</strong> updated.'),
    ]
