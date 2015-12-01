def test_dashboard_nologin(client):
    response = client.get('/dashboard/', follow=True)
    assert response.redirect_chain == [
        ('http://testserver/accounts/login/?next=/dashboard/', 302),
    ]


def test_dashboard_bare(bare_user_client, parser):
    response = bare_user_client.get('/dashboard/')
    body = parser.parse(response)
    assert body.cssselect('a[href="/accounts/profile/"]'), (
        'should contain link to profile edit'
    )
    assert not body.cssselect('a[href="/proposals/create/"]'), (
        'should not be able to create a proposal (needs to fill profile first)'
    )


def test_dashboard(user_client, parser):
    response = user_client.get('/dashboard/')
    body = parser.parse(response)
    assert body.cssselect('a[href="/accounts/profile/"]'), (
        'should contain link to profile edit'
    )
    # assert body.cssselect('a[href="/proposals/create/"]'), (
    #     'should be able to create a proposal'
    # )


def test_profile_nologin(client):
    response = client.get('/accounts/profile/', follow=True)
    assert response.redirect_chain == [
        ('http://testserver/accounts/login/?next=/accounts/profile/', 302),
    ]


def test_profile_get(user_client, parser):
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
    assert response.redirect_chain == [('http://testserver/dashboard/', 302)]
