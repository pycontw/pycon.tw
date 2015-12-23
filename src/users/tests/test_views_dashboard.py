import pytest

from proposals.models import TalkProposal, TutorialProposal


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
