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
    response = client.get('/en-us/dashboard/', follow=True)
    assert response.redirect_chain == [
        ('/en-us/accounts/login/?next=/en-us/dashboard/', 302),
    ]


def test_dashboard_bare(bare_user_client):
    response = bare_user_client.get('/en-us/dashboard/')
    assert response.status_code == 200


def test_dashboard_bare_ui(bare_user_client, parser):
    response = bare_user_client.get('/en-us/dashboard/')
    body = parser.parse(response)
    assert body.cssselect('a[href="/en-us/accounts/profile/"]'), (
        'should contain link to profile edit'
    )
    assert not body.cssselect('a[href="/en-us/proposals/submit/"]'), (
        'should not be able to submit a proposal (needs to fill profile first)'
    )


def test_dashboard(user_client):
    response = user_client.get('/en-us/dashboard/')
    assert response.status_code == 200


def test_dashboard_ui(user_client, parser):
    response = user_client.get('/en-us/dashboard/')
    body = parser.parse(response)
    assert body.cssselect('a[href="/en-us/accounts/profile/"]'), (
        'should contain link to profile edit'
    )
    assert body.cssselect('a[href="/en-us/proposals/submit/"]'), (
        'should be able to submit a proposal'
    )
    assert len(body.cssselect('.proposal')) == 0, 'no submitted proposals'


@pytest.mark.xfail
def test_dashboard_proposal_list(user_client, proposals, parser):
    response = user_client.get('/en-us/dashboard/')
    body = parser.parse(response)
    assert body.cssselect('a[href="/en-us/accounts/profile/"]'), (
        'should contain link to profile edit'
    )
    assert body.cssselect('a[href="/en-us/proposals/submit/"]'), (
        'should be able to submit a proposal'
    )

    elements = [parser.arrange(e) for e in body.cssselect('.proposal-title')]
    assert len(elements) == 6

    template = (
        '<h4 class="proposal-title">'
        '<a href="/en-us/proposals/{type}/{pk}/edit/">{title}</a></h4>'
    )

    # The first three proposals are for talks.
    assert elements[:3] == [
        parser.arrange(template.format(
            pk=proposal.pk, type='talk', title=proposal.title,
        ))
        for proposal in proposals['talk']
    ]

    # The latter three proposals are for tutorials.
    assert elements[-3:] == [
        parser.arrange(template.format(
            pk=proposal.pk, type='tutorial', title=proposal.title,
        ))
        for proposal in proposals['tutorial']
    ]
