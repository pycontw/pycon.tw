import pytest


def test_talk_list(client, accepted_talk_proposal, sponsored_block_event):
    r = client.get('/en-us/events/talks/')
    assert r.status_code == 200


@pytest.mark.parametrize('pk,status', [(42, 200), (9, 404)])
def test_talk_detail(client, accepted_talk_proposal, pk, status):
    r = client.get('/en-us/events/talk/{pk}/'.format(pk=pk))
    assert r.status_code == status


@pytest.mark.parametrize('pk,status', [(918, 301), (819, 404)])
def test_sponsored_event_redirect(client, sponsored_block_event, pk, status):
    r = client.get('/en-us/events/sponsored/{pk}/'.format(pk=pk))
    assert r.status_code == status


@pytest.mark.parametrize('slug,status', [
    ('camera-engine', 200),
    ('carmona-eugene', 404),
])
def test_sponsored_event_detail(client, sponsored_block_event, slug, status):
    r = client.get('/en-us/events/talk/sponsored/{slug}/'.format(slug=slug))
    assert r.status_code == status


def test_schedule(client, parser, schedule):
    r = client.get('/en-us/events/schedule/')
    body = parser.parse(r)

    # Make sure every cross-page intra-site link is good.
    link_tags = body.cssselect('a[href^="/"]')
    assert len(link_tags) != 0
    for tag in link_tags:
        assert client.get(tag.get('href'), follow=True).status_code == 200
