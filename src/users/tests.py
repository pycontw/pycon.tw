import re

import pytest

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import mail, signing
from django.test import override_settings

from proposals.models import TalkProposal, TutorialProposal


User = get_user_model()


@pytest.fixture
def proposals(user):
    for t in ['Fluidity Shoes', 'Post-rifle cardboard', 'Face forwards pen']:
        TalkProposal.objects.create(submitter=user, title=t)

    for t in ['Crypto-bicycle', 'receding tattoo', 'A.I. monofilament']:
        TutorialProposal.objects.create(submitter=user, title=t)

    proposals = {
        'talk': TalkProposal.objects.all(),
        'tutorial': TutorialProposal.objects.all(),
    }
    return proposals


def test_signup_login(bare_user_client):
    """If the request is already authenticated, the signup view should
    redirect it to the dashboard.
    """
    response = bare_user_client.get('/accounts/signup/', follow=True)
    assert response.redirect_chain == [('/dashboard/', 302)]


def test_signup_get(client):
    response = client.get('/accounts/signup/')
    assert response.status_code == 200


@pytest.mark.django_db
@override_settings(     # Make sure we don't really send an email.
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='dev@pycon.tw',
)
def test_signup_post(client, parser):
    """If the signup is successful, the user instance should be created,
    and a confirmation email sent.

    The viewer should be redirected to the homepage.
    """
    response = client.post('/accounts/signup/', {
        'email': 'user@user.me',
        'password1': '7K50M',
        'password2': '7K50M',
    }, follow=True)
    assert response.redirect_chain == [('/', 302)]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [(messages.SUCCESS, (
        'An email has been sent to your email. Please follow instructions in '
        'the email to complete your signup.'
    ))]

    user = User.objects.get(email='user@user.me')
    assert not user.is_active

    assert len(mail.outbox) == 1

    email = mail.outbox[0]
    assert email.from_email == 'dev@pycon.tw'
    assert email.to == ['user@user.me']
    assert email.subject == 'Complete your registration on tw.pycon.org'

    message_match = re.match(
        r'^Go here: http://testserver/accounts/activate/(?P<key>[-:\w]+)/$',
        email.body.strip(),
    )
    assert message_match, email.body.strip()
    assert user.email == signing.loads(
        message_match.group('key'),
        salt='pycontw', max_age=86400,
    )

    assert len(email.alternatives) == 1
    assert len(email.alternatives[0]) == 2
    assert email.alternatives[0][-1] == 'text/html'

    body = parser.parse(text=email.alternatives[0][0])
    link_tag = body.cssselect('#activation-link')[0]
    assert link_tag.get('target') == '_blank'
    assert link_tag.get('href') == link_tag.text.strip()

    link_match = re.match(
        r'^http://testserver/accounts/activate/(?P<key>[-:\w]+)/$',
        link_tag.get('href'),
    )
    assert link_match, link_tag.get('href')
    assert user.email == signing.loads(
        link_match.group('key'),
        salt='pycontw', max_age=86400,
    )


def test_signup_duplicate(bare_user, client, parser):
    response = client.post('/accounts/signup/', {
        'email': 'user@user.me',
        'password1': '7K50M',
        'password2': '7K50M',
    })
    assert response.status_code == 200

    body = parser.parse(response)
    assert [tag.text for tag in body.cssselect('.errorlist > li')] == [
        'A user with that email already exists.'
    ]


def test_activate(inactive_user, client):
    """A valid activation should result in the user logged-in, redirected to
    dashboard, and getting a success message.
    """
    key = inactive_user.get_activation_key()
    link = '/accounts/activate/{key}/'.format(key=key)

    response = client.get(link, follow=True)
    assert response.redirect_chain == [('/dashboard/', 302)]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS, 'Signup successful. You are now logged in.'),
    ]


def test_activate_logged_in(inactive_user, another_user, another_user_client):
    """User is logged-out when clicking an activation link.
    """
    # Before the activation view, client belongs to another_user.
    assert another_user_client.session['_auth_user_id'] == str(another_user.pk)

    key = inactive_user.get_activation_key()
    link = '/accounts/activate/{key}/'.format(key=key)

    response = another_user_client.get(link, follow=True)
    assert response.redirect_chain == [('/dashboard/', 302)]

    # After the activation view, another_user should be logged out, and
    # inactive_user (owner of the activation key) is logged in instead.
    assert response.client.session['_auth_user_id'] == str(inactive_user.pk)

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS, 'Signup successful. You are now logged in.'),
    ]


def test_activate_invalid(inactive_user, client):
    """Using an invalid activation code just results in 404.
    """
    key = inactive_user.get_activation_key().swapcase()
    link = '/accounts/activate/{key}/'.format(key=key)

    response = client.get(link)
    assert response.status_code == 404


@override_settings(USER_ACTIVATION_EXPIRE_SECONDS=0)
def test_activate_expired(inactive_user, client):
    """Using an expired activation code just results in 404.
    """
    key = inactive_user.get_activation_key()
    link = '/accounts/activate/{key}/'.format(key=key)

    response = client.get(link)
    assert response.status_code == 404


def test_dashboard_nologin(client):
    response = client.get('/dashboard/', follow=True)
    assert response.redirect_chain == [
        ('/accounts/login/?next=/dashboard/', 302),
    ]


def test_dashboard_bare(bare_user_client):
    response = bare_user_client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_bare_ui(bare_user_client, parser):
    response = bare_user_client.get('/dashboard/')
    body = parser.parse(response)
    assert body.cssselect('a[href="/accounts/profile/"]'), (
        'should contain link to profile edit'
    )
    assert not body.cssselect('a[href="/proposals/submit/"]'), (
        'should not be able to submit a proposal (needs to fill profile first)'
    )


def test_dashboard(user_client):
    response = user_client.get('/dashboard/')
    assert response.status_code == 200


def test_dashboard_ui(user_client, parser):
    response = user_client.get('/dashboard/')
    body = parser.parse(response)
    assert body.cssselect('a[href="/accounts/profile/"]'), (
        'should contain link to profile edit'
    )
    assert body.cssselect('a[href="/proposals/submit/"]'), (
        'should be able to submit a proposal'
    )
    assert len(body.cssselect('.proposal')) == 0, 'no submitted proposals'


def test_dashboard_proposal_list(user_client, proposals, parser):
    response = user_client.get('/dashboard/')
    body = parser.parse(response)
    assert body.cssselect('a[href="/accounts/profile/"]'), (
        'should contain link to profile edit'
    )
    assert body.cssselect('a[href="/proposals/submit/"]'), (
        'should be able to submit a proposal'
    )

    elements = [parser.arrange(e) for e in body.cssselect('.proposal')]
    assert len(elements) == 6

    template = (
        '<div class="proposal"><a href="/proposals/{type}/{pk}/edit/">'
        'Edit <strong>{title}</strong></a></div>'
    )
    assert elements[:3] == [
        parser.arrange(template.format(
            pk=proposal.pk, type='talk', title=proposal.title,
        ))
        for proposal in proposals['talk']
    ]
    assert elements[-3:] == [
        parser.arrange(template.format(
            pk=proposal.pk, type='tutorial', title=proposal.title,
        ))
        for proposal in proposals['tutorial']
    ]


def test_profile_nologin(client):
    response = client.get('/accounts/profile/', follow=True)
    assert response.redirect_chain == [
        ('/accounts/login/?next=/accounts/profile/', 302),
    ]


def test_profile_get(user_client):
    response = user_client.get('/accounts/profile/')
    assert response.status_code == 200


def test_profile_get_ui(user_client, parser):
    response = user_client.get('/accounts/profile/')
    body = parser.parse(response)

    form = body.get_element_by_id('user_profile_update_form')
    assert form.cssselect('a[href="/dashboard/"]'), (
        'should contain cancel link'
    )
    assert form.cssselect('button[type="submit"]'), (
        'should contain submit button'
    )


def test_profile_post(user_client):
    response = user_client.post('/accounts/profile/', {
        'speaker_name': 'User',
        'bio': 'Girl meta-dome kanji-space shoes Chiba rifle sub-orbital.',
    }, follow=True)
    assert response.redirect_chain == [('/dashboard/', 302)]
