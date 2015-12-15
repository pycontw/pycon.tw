import pytest

from django.contrib.auth import get_user_model

from proposals.models import TalkProposal


User = get_user_model()


@pytest.fixture
def proposals(user):
    TalkProposal.objects.create(submitter=user, title='Fluidity Shoes')
    TalkProposal.objects.create(submitter=user, title='Post-rifle cardboard')
    TalkProposal.objects.create(submitter=user, title='Face forwards pen')

    proposals = TalkProposal.objects.all()
    return proposals


def test_signup_login(bare_user_client):
    """If the request is already authenticated, the signup view should
    redirect it to the dashboard.
    """
    response = bare_user_client.get('/accounts/signup/', follow=True)
    assert response.redirect_chain == [('http://testserver/dashboard/', 302)]


def test_signup_get(client):
    response = client.get('/accounts/signup/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_post(client):
    """If the signup is successful, the user should be created, with the
    request logged-in and redirected to dashboard.
    """
    response = client.post('/accounts/signup/', {
        'email': 'user@user.me',
        'password1': '7K50M',
        'password2': '7K50M',
    }, follow=True)
    assert response.redirect_chain == [('http://testserver/dashboard/', 302)]
    assert User.objects.filter(email='user@user.me').exists()


def test_signup_duplicate(bare_user, client):
    response = client.post('/accounts/signup/', {
        'email': 'user@user.me',
        'password1': '7K50M',
        'password2': '7K50M',
    })
    assert response.status_code == 200


def test_dashboard_nologin(client):
    response = client.get('/dashboard/', follow=True)
    assert response.redirect_chain == [
        ('http://testserver/accounts/login/?next=/dashboard/', 302),
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
    assert len(elements) == 3

    template = (
        '<div class="proposal"><a href="/proposals/{pk}/edit/">'
        'Edit <strong>{title}</strong></a></div>'
    )
    assert elements == [
        parser.arrange(template.format(pk=proposal.pk, title=proposal.title))
        for proposal in proposals
    ]


def test_profile_nologin(client):
    response = client.get('/accounts/profile/', follow=True)
    assert response.redirect_chain == [
        ('http://testserver/accounts/login/?next=/accounts/profile/', 302),
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
    assert response.redirect_chain == [('http://testserver/dashboard/', 302)]
