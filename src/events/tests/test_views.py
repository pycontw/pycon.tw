import pytest

from django.conf import settings


@pytest.mark.skipif(
    not settings.EVENTS_PUBLISHED,
    reason='event pages not required yet',
)
def test_talk_list(client, accepted_talk_proposal, sponsored_block_event):
    r = client.get('/en-us/events/talks/')
    assert r.status_code == 200


@pytest.mark.skipif(
    not settings.EVENTS_PUBLISHED,
    reason='event pages not required yet',
)
@pytest.mark.parametrize('pk,status', [(42, 200), (9, 404)])
def test_talk_detail(client, accepted_talk_proposal, pk, status):
    r = client.get('/en-us/events/talk/{pk}/'.format(pk=pk))
    assert r.status_code == status


@pytest.mark.skipif(
    not settings.EVENTS_PUBLISHED,
    reason='event pages not required yet',
)
@pytest.mark.parametrize('slug,status', [
    ('camera-engine', 200),
    ('carmona-eugene', 404),
])
def test_sponsored_event_detail(client, sponsored_block_event, slug, status):
    r = client.get('/en-us/events/talk/sponsored/{slug}/'.format(slug=slug))
    assert r.status_code == status
