import pytest

from django.contrib.auth import get_user_model
from django.test.html import parse_html


User = get_user_model()


class HTMLParser:

    def parse(self, response=None, *, text=None, status_code=200):
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
        fragment = lxml_html.fragment_fromstring(text, create_parent=True)
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


@pytest.fixture
def inactive_user(db):
    try:
        user = User.objects.get(email='user@user.me')
    except User.DoesNotExist:
        user = User.objects.create_user(
            email='user@user.me',
            password='7K50<31',
        )
    return user


@pytest.fixture
def bare_user(inactive_user):
    user = User.objects.get(email='user@user.me')
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def user(bare_user):
    user = User.objects.get(email='user@user.me')
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
