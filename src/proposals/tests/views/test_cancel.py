import pytest

from django.conf import settings
from django.contrib import messages

from proposals.models import TalkProposal, TutorialProposal
from core.utils import set_registry


def test_talk_proposal_cancel_login(client):
    response = client.get('/en-us/proposals/talk/42/cancel/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/login/?next=/en-us/proposals/talk/42/cancel/', 302),
    ]


def test_tutorial_proposal_cancel_login(client):
    response = client.get('/en-us/proposals/tutorial/42/cancel/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/login/?next=/en-us/proposals/tutorial/42/cancel/',
         302),
    ]


@pytest.mark.parametrize('method', ['get', 'post'])
@set_registry(**{'proposals.withdrawable': True})
def test_talk_proposal_cancel_denied(bare_user_client, method):
    response = getattr(bare_user_client, method)(
        '/en-us/proposals/talk/42/cancel/',
    )
    assert response.status_code == 403


@pytest.mark.parametrize('method', ['get', 'post'])
@set_registry(**{'proposals.withdrawable': True})
def test_tutorial_proposal_cancel_denied(bare_user_client, method):
    response = getattr(bare_user_client, method)(
        '/en-us/proposals/tutorial/42/cancel/',
    )
    assert response.status_code == 403


@set_registry(**{'proposals.withdrawable': True})
def test_talk_proposal_cancel_get(agreed_user_client, talk_proposal):
    """The cancel view should not allow GET, only POST.
    """
    response = agreed_user_client.get('/en-us/proposals/talk/42/cancel/')
    assert response.status_code == 405


@set_registry(**{'proposals.withdrawable': True})
def test_tutorial_proposal_cancel_get(agreed_user_client, tutorial_proposal):
    """The cancel view should not allow GET, only POST.
    """
    response = agreed_user_client.get('/en-us/proposals/tutorial/42/cancel/')
    assert response.status_code == 405


@set_registry(**{'proposals.withdrawable': True})
def test_talk_proposal_cancel_not_owned(another_agreed_user_client, talk_proposal):
    response = another_agreed_user_client.post('/en-us/proposals/talk/42/cancel/')
    assert response.status_code == 404


@set_registry(**{'proposals.withdrawable': True})
def test_tutorial_proposal_cancel_not_owned(
        another_agreed_user_client, tutorial_proposal):
    response = another_agreed_user_client.post('/en-us/proposals/tutorial/42/cancel/')
    assert response.status_code == 404


@set_registry(**{'proposals.withdrawable': False})
def test_talk_proposal_cancel_disabled(agreed_user_client, talk_proposal):
    response = agreed_user_client.post('/en-us/proposals/talk/42/cancel/')
    assert response.status_code == 404


@set_registry(**{'proposals.withdrawable': True})
def test_talk_proposal_cancel(agreed_user_client, talk_proposal):
    assert not talk_proposal.cancelled

    response = agreed_user_client.post('/en-us/proposals/talk/42/cancel/', {
        'cancelled': True,
    }, follow=True)
    assert response.redirect_chain == [('/en-us/dashboard/', 302)], (
        response.context['form'].errors
    )

    assert TalkProposal.objects.get(pk=42).cancelled

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.INFO,
         'Talk proposal '
         '<strong>Beyond the Style Guides&lt;br&gt;</strong> withdrawn.'),
    ]


@set_registry(**{'proposals.withdrawable': True})
def test_talk_proposal_reactivate(agreed_user_client, cancelled_talk_proposal):
    assert cancelled_talk_proposal.cancelled

    response = agreed_user_client.post('/en-us/proposals/talk/42/cancel/', {
        'cancelled': '',
    }, follow=True)
    assert response.redirect_chain == [('/en-us/dashboard/', 302)], (
        response.context['form'].errors
    )

    assert not TalkProposal.objects.get(pk=42).cancelled

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS,
         'Talk proposal '
         '<strong>Beyond the Style Guides&lt;br&gt;</strong> reactivated.'),
    ]


@set_registry(**{'proposals.withdrawable': False})
def test_tutorial_proposal_cancel_disabled(agreed_user_client, tutorial_proposal):
    response = agreed_user_client.post('/en-us/proposals/tutorial/42/cancel/')
    assert response.status_code == 404


@set_registry(**{'proposals.withdrawable': True})
def test_tutorial_proposal_cancel(agreed_user_client, tutorial_proposal):
    assert not tutorial_proposal.cancelled

    response = agreed_user_client.post('/en-us/proposals/tutorial/42/cancel/', {
        'cancelled': True,
    }, follow=True)
    assert response.redirect_chain == [('/en-us/dashboard/', 302)], (
        response.context['form'].errors
    )

    assert TutorialProposal.objects.get(pk=42).cancelled

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.INFO,
         'Tutorial proposal '
         '<strong>Beyond the Style Guides&lt;br&gt;</strong> withdrawn.'),
    ]


@set_registry(**{'proposals.withdrawable': True})
def test_tutorial_proposal_reactivate(
        agreed_user_client, cancelled_tutorial_proposal):
    assert cancelled_tutorial_proposal.cancelled

    response = agreed_user_client.post('/en-us/proposals/tutorial/42/cancel/', {
        'cancelled': '',
    }, follow=True)
    assert response.redirect_chain == [('/en-us/dashboard/', 302)], (
        response.context['form'].errors
    )

    assert not TutorialProposal.objects.get(pk=42).cancelled

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS,
         'Tutorial proposal '
         '<strong>Beyond the Style Guides&lt;br&gt;</strong> reactivated.'),
    ]
