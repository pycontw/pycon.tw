import pytest
from django.contrib.auth.models import Group
from django.urls import reverse


@pytest.fixture
def auth_user(django_user_model):
    return django_user_model.objects.create(
        email="test_auth@example.com",
        speaker_name="Auth User",
        verified=True,
        is_active=True,
    )


@pytest.mark.django_db
def test_user_list_with_role_filter_exact_match(api_client, django_user_model, auth_user):
    group = Group.objects.create(name='Reviewer')
    reviewer = django_user_model.objects.create(
        email="reviewer@example.com",
        speaker_name="Reviewer Name",
        bio="Some bio",
        verified=True,
        is_active=True,
    )
    reviewer.groups.add(group)

    api_client.force_authenticate(user=auth_user)

    django_user_model.objects.create(
        email="other@example.com",
        speaker_name="Other User",
        bio="Other bio",
        verified=True,
        is_active=True,
    )

    url = reverse('user_list')
    response = api_client.get(url, {'role': 'Reviewer'})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]['full_name'] == reviewer.get_full_name()
    assert data[0]['bio'] == reviewer.bio


@pytest.mark.django_db
def test_user_list_excludes_unverified_users(api_client, django_user_model):
    group = Group.objects.create(name='Reviewer')
    unverified_user = django_user_model.objects.create(
        email="unverified@example.com",
        speaker_name="Not Verified",
        bio="Nope",
        is_active=True,
        verified=False,
    )
    unverified_user.groups.add(group)

    api_client.force_authenticate(user=unverified_user)

    url = reverse('user_list')
    response = api_client.get(url, {'role': 'Reviewer'})
    assert response.status_code == 200
    assert response.json() == []



@pytest.mark.django_db
def test_user_list_with_invalid_role_returns_400(api_client, django_user_model):
    user = django_user_model.objects.create(
        email="someuser@example.com",
        speaker_name="Some User",
        bio="Bio text",
        verified=True,
        is_active=True,
    )

    api_client.force_authenticate(user=user)

    url = reverse('user_list')
    response = api_client.get(url, {'role': 'NotARealRole'})
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_list_without_role_returns_400(api_client, django_user_model):
    user = django_user_model.objects.create(
        email="someuser@example.com",
        speaker_name="Some User",
        bio="Bio text",
        verified=True,
        is_active=True,
    )

    api_client.force_authenticate(user=user)

    url = reverse('user_list')
    response = api_client.get(url)
    assert response.status_code == 400
