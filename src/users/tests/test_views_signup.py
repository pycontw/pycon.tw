import pytest

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from django.test import override_settings


User = get_user_model()


def test_signup_login(bare_user_client):
    """If the request is already authenticated, the signup view should
    redirect it to the dashboard.
    """
    response = bare_user_client.get('/en-us/accounts/signup/', follow=True)
    assert response.redirect_chain[0] == ('/en-us/dashboard/', 302)


def test_signup_get(client):
    response = client.get('/en-us/accounts/signup/')
    assert response.status_code == 200


@pytest.mark.django_db
@override_settings(     # Make sure we don't really send an email.
    SECRET_KEY='Footage order-flow long-chain hydrocarbons hacker',
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='dev@pycon.tw',
)
def test_signup_post(client, parser):
    """If the signup is successful, the user instance should be created,
    and a verificaion email sent.

    The viewer should be logged in, and redirected to the dashboard.
    """
    response = client.post('/en-us/accounts/signup/', {
        'email': 'user@user.me',
        'password1': '7K50M',
        'password2': '7K50M',
    }, follow=True)
    assert response.redirect_chain[0] == ('/en-us/dashboard/', 302)

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS, 'Sign up successful. You are now logged in.'),
    ]

    user = User.objects.get(email='user@user.me')
    assert not user.verified

    assert len(mail.outbox) == 1

    email = mail.outbox[0]
    assert email.from_email == 'dev@pycon.tw'
    assert email.to == ['user@user.me']
    assert email.subject == 'Verify your email address on testserver'


def test_signup_duplicate(bare_user, client):
    response = client.post('/en-us/accounts/signup/', {
        'email': 'user@user.me',
        'password1': '7K50M',
        'password2': '7K50M',
    })
    assert response.status_code == 200


def test_verify(bare_user, bare_user_client):
    """A valid verification should result in the user getting a success
    message, and redirected to dashboard.
    """
    key = bare_user.get_verification_key()
    link = '/en-us/accounts/verify/{key}/'.format(key=key)

    response = bare_user_client.get(link, follow=True)
    assert response.redirect_chain[0] == ('/en-us/dashboard/', 302)

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS, 'Email verification successful.'),
    ]


def test_verify_invalid(bare_user, client):
    """Using an invalid verification code just results in 404.
    """
    # We use reverse to make sure we have the right link (but wrong key).
    response = client.get(reverse('user_verify', kwargs={
        'verification_key': bare_user.get_verification_key().swapcase(),
    }))
    assert response.status_code == 404


def test_verification_login(client):
    response = client.get('/en-us/accounts/verification-request/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/login/?next=/en-us/accounts/verification-request/',
         302),
    ]


def test_verification_get(bare_user_client):
    response = bare_user_client.get('/en-us/accounts/verification-request/')
    assert response.status_code == 405


def test_verification_post(user_client):
    response = user_client.post(
        '/en-us/accounts/verification-request/',
        follow=True,
    )
    assert response.redirect_chain == [('/en-us/dashboard/', 302)]
