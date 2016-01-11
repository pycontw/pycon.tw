import pytest

from django.contrib import messages
from django.contrib.auth import get_user_model


User = get_user_model()


def test_profile_nologin(client):
    response = client.get('/en-us/accounts/profile/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/login/?next=/en-us/accounts/profile/', 302),
    ]


def test_profile_get(user_client):
    response = user_client.get('/en-us/accounts/profile/')
    assert response.status_code == 200


@pytest.mark.xfail
def test_profile_get_ui(user_client, parser):
    response = user_client.get('/en-us/accounts/profile/')
    body = parser.parse(response)

    form = body.get_element_by_id('user_profile_update_form')
    assert form.cssselect('a[href="/en-us/dashboard/"]'), (
        'should contain cancel link'
    )
    assert form.cssselect('button[type="submit"]'), (
        'should contain submit button'
    )


def test_profile_post(user_client):
    response = user_client.post('/en-us/accounts/profile/', {
        'speaker_name': 'User',
        'bio': 'Girl meta-dome kanji-space shoes Chiba rifle sub-orbital.',
    }, follow=True)
    assert response.redirect_chain == [('/en-us/dashboard/', 302)]


def test_password_change_done(user_client):
    response = user_client.get(
        '/en-us/accounts/password-reset/done/', follow=True,
    )
    assert response.redirect_chain == [('/en-us/accounts/login/', 302)]

    msgs = [(m.level, m.message) for m in response.context['messages']]
    assert msgs == [
        (messages.SUCCESS,
         'An email is sent to your email account. Please check your inbox '
         'for furthur instructions to reset your password.'),
    ]
