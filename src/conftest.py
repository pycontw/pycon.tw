import collections
import six

import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test.html import parse_html

from proposals.models import TalkProposal


class HTMLParser:

    def parse(
            self, response=None, *,
            text=None, status_code=200, create_parent=True):
        if response is not None and text is not None:
            raise ValueError(
                'Provide exactly one of "response" and "text" to parse.',
            )
        if response is not None:
            if status_code is not None:
                assert response.status_code == status_code
            text = response.content
        pytest.importorskip('cssselect')
        lxml_html = pytest.importorskip('lxml.html')
        fragment = lxml_html.fragment_fromstring(
            text, create_parent=create_parent,
        )
        return fragment

    def arrange(self, element):
        """Arrange an HTML node for comparison.

        This method uses Django's ``parse_html`` testing utility to build
        an HTML node for asserting purposes. Usage::

            def test_div_foo(client, parser):
                body = parser.parse(client.get('/foo/'))
                expected = parser.arrange('<body><div>foo</div></body>')
                assert parser.arrage(body) == expected

        :param element: An HTML element. This can be either an lxml element,
            or a string containing valid HTML. If an lxml element is passed
            in, ``lxml.etree.tostring`` is used to convert the element to
            string.
        """
        lxml_etree = pytest.importorskip('lxml.etree')
        if isinstance(element, lxml_etree.ElementBase):
            element = lxml_etree.tostring(element)
        if not isinstance(element, str):
            element = element.decode('utf-8')
        return parse_html(element)


@pytest.fixture
def parser():
    return HTMLParser()


class DjangoUtils:
    """Test utilities for testing Django things.
    """
    def to_list(self, qs, transform=repr):
        """Convert a queryset to list.

        This uses a similar algorithm to Django's `assertQuerySetEqual` to
        convert the queryset, but leave the asserting part to pytest.
        """
        items = six.moves.map(transform, qs)
        return list(items)

    def to_counter(self, qs, transform=repr):
        """Convert a queryset to a `collections.Counter`.

        This uses a similar algorithm to Django's `assertQuerySetEqual` to
        convert the queryset, but leave the asserting part to pytest.
        """
        items = six.moves.map(transform, qs)
        return collections.Counter(items)


@pytest.fixture
def djutils():
    return DjangoUtils()


@pytest.fixture
def bare_user(db):
    user = get_user_model().objects.create_user(
        email='user@user.me', password='7K50<31',
    )
    return user


@pytest.fixture(params=[AnonymousUser, 'bare_user'])
def invalid_user(request, bare_user):
    if callable(request.param):
        return request.param()
    return locals()[request.param]


@pytest.fixture
def user(bare_user):
    user = get_user_model().objects.get(email='user@user.me')
    user.verified = True
    user.speaker_name = 'User'
    user.bio = 'Wonton soup semiotics warehouse neural urban physical-ware.'
    user.save()
    return user


@pytest.fixture
def bare_user_client(bare_user, client):
    client.login(email='user@user.me', password='7K50<31')
    return client


@pytest.fixture
def user_client(user, bare_user_client):
    return bare_user_client


@pytest.fixture
def another_bare_user(db):
    user = get_user_model().objects.create_user(
        email='another@ayatsuji.itou',
        password='7uk1T0n01sY',
    )
    return user


@pytest.fixture
def another_user(another_bare_user):
    user = get_user_model().objects.get(email='another@ayatsuji.itou')
    user.speaker_name = 'Misaki Mei'
    user.bio = 'Neon marketing office assault kanji into meta-face.'
    user.verified = True
    user.save()
    return user


@pytest.fixture
def another_user_client(another_user, client):
    client.login(email='another@ayatsuji.itou', password='7uk1T0n01sY')
    return client


@pytest.fixture
def admin_user(db):
    user = get_user_model().objects.create_superuser(
        email='admin@adm.in', password='7K50<31',
    )
    assert user.is_superuser
    return user


@pytest.fixture
def admin_client(admin_user, client):
    client.login(email='admin@adm.in', password='7K50<31')
    return client


@pytest.fixture
def talk_proposal(user):
    proposal = TalkProposal.objects.create(
        id=42,
        submitter=user,
        title='Beyond the Style Guides<br>',
        language='ZHEN',
    )
    return proposal


@pytest.fixture
def accepted_talk_proposal(talk_proposal):
    talk_proposal.accepted = True
    talk_proposal.save()
    return talk_proposal
