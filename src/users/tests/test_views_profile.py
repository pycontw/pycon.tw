from django.contrib.auth import get_user_model


User = get_user_model()


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
