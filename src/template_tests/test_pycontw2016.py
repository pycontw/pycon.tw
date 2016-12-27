import re

import pytest

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail, signing
from django.test import override_settings


pytestmark = pytest.mark.skipif(
    settings.CONFERENCE_DEFAULT_SLUG != 'pycontw-2016',
    reason='Not current conference',
)


User = get_user_model()


def test_schedule(client, parser, schedule):
    r = client.get('/en-us/events/schedule/')
    body = parser.parse(r)

    # Make sure every cross-page intra-site link is good.
    link_tags = body.cssselect('a[href^="/"]')
    assert len(link_tags) != 0
    for tag in link_tags:
        assert client.get(tag.get('href'), follow=True).status_code == 200


@pytest.mark.django_db
@override_settings(     # Make sure we don't really send an email.
    SECRET_KEY='Footage order-flow long-chain hydrocarbons hacker',
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='dev@pycon.tw',
)
def test_signup_post(client, parser):
    """Check the verification email has correct format.
    """
    client.post('/en-us/accounts/signup/', {
        'email': 'user@user.me',
        'password1': '7K50M',
        'password2': '7K50M',
    }, follow=True)

    user = User.objects.get(email='user@user.me')
    email = mail.outbox[0]

    # The message does contain the activation link
    message_has_verification_link = re.search(
        r'^\s*http://testserver/en-us/accounts/verify/(?P<key>[-:\w]+)/$',
        email.body.strip(),
        re.MULTILINE
    )
    # The message hints the email in use
    message_has_account_email = user.email in email.body

    assert message_has_verification_link, email.body.strip()
    assert message_has_account_email, email.body.strip()
    assert user.email == signing.loads(
        message_has_verification_link.group('key'),
        salt='Footage order-flow long-chain hydrocarbons hacker',
    )
    assert not email.alternatives


@pytest.mark.usefixtures('bare_user')
def test_signup_duplicate(client, parser):
    response = client.post('/en-us/accounts/signup/', {
        'email': 'user@user.me',
        'password1': '7K50M',
        'password2': '7K50M',
    })

    body = parser.parse(response)
    errored_blocks = body.cssselect('.has-error')
    assert [e.get('id') for e in errored_blocks] == ['div_id_email']
    assert [
        parser.arrange(e)
        for e in errored_blocks[0].cssselect('.help-block')
    ] == [
        parser.arrange(
            '<p id="error_1_id_email" class="help-block">'
            '<strong>A user with that email already exists.</strong>'
            '</p>'
        )
    ]
