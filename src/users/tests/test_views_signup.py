import re

import pytest

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import mail, signing
from django.test import override_settings


User = get_user_model()


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
    assert response.redirect_chain == [('/accounts/login/', 302)]

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
    assert not email.alternatives


def test_signup_duplicate(bare_user, client, parser):
    response = client.post('/accounts/signup/', {
        'email': 'user@user.me',
        'password1': '7K50M',
        'password2': '7K50M',
    })
    assert response.status_code == 200

    body = parser.parse(response)
    errored_blocks = body.cssselect('.has-error')
    assert [e.get('id') for e in errored_blocks] == ['div_id_email']
    assert [
        parser.arrange(e)
        for e in errored_blocks[0].cssselect('.help-block')
    ] == [
        parser.arrange(
            '<span id="error_1_id_email" class="help-block">'
            '<strong>A user with that email already exists.</strong>'
            '</span>'
        )
    ]


def test_activate(inactive_user, client):
    """A valid activation should result in the user logged-in, redirected to
    dashboard, and getting a success message.
    """
    key = inactive_user.get_activation_key()
    link = '/accounts/activate/{key}/'.format(key=key)

    response = client.get(link, follow=True)
    assert response.redirect_chain == [('/accounts/login/', 302)]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS, 'Signup successful. You can log in now.'),
    ]


def test_activate_logged_in(inactive_user, another_user, another_user_client):
    """User is logged-out when clicking an activation link.
    """
    # Before the activation view, client belongs to another_user.
    assert another_user_client.session['_auth_user_id'] == str(another_user.pk)

    key = inactive_user.get_activation_key()
    link = '/accounts/activate/{key}/'.format(key=key)

    response = another_user_client.get(link, follow=True)
    assert response.redirect_chain == [('/accounts/login/', 302)]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS, 'Signup successful. You can log in now.'),
    ]

    # After the activation view, another_user should be logged out, and
    # inactive_user (owner of the activation key) is logged in instead.
    assert '_auth_user_id' not in response.client.session


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
