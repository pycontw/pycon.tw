import pytest
from django.contrib.auth.models import Group
from django.urls import reverse


@pytest.mark.django_db
def test_user_list_with_role_filter_exact_match(api_client, django_user_model):
    group = Group.objects.create(name='Reviewer')
    user = django_user_model.objects.create(
        email="reviewer@example.com",
        speaker_name="Reviewer Name",
        bio="Some bio",
        verified=True,
        is_active=True,
    )
    user.groups.add(group)

    api_client.force_authenticate(user=user)

    url = reverse('user_list')
    response = api_client.get(url, {'role': 'Reviewer'})
    assert response.status_code == 200

    data = response.json()
    assert data == [
        {
            'full_name': user.get_full_name(),
            'bio': user.bio,
            'photo_url': None,
            'facebook_profile_url': user.facebook_profile_url,
            'twitter_profile_url': user.twitter_profile_url,
            'github_profile_url': user.github_profile_url,
        }
    ]


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
