import pytest

from django.contrib.auth import get_user_model


User = get_user_model()


class HTMLParser:
    def parse(self, response, status_code=200):
        if status_code is not None:
            assert response.status_code == status_code
        from lxml.html import fragment_fromstring
        fragment = fragment_fromstring(response.content, create_parent='body')
        return fragment


@pytest.fixture
def parser():
    return HTMLParser()


@pytest.fixture
def bare_user(db):
    try:
        user = User.objects.get(email='user@user.me')
    except User.DoesNotExist:
        user = User.objects.create_user(
            email='user@user.me',
            password='7K50<31',
        )
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
