import pytest
from django.contrib.auth.models import Group
from django.urls import reverse


@pytest.mark.django_db
def test_user_list_returns_all_users(client, django_user_model):
    user = django_user_model.objects.create(
        email="test@example.com",
        speaker_name="Test User",
        bio="Bio text",
        verified=True,
        is_active=True,
    )

    from core.models import Token
    token, _ = Token.objects.get_or_create(user=user)

    url = reverse('user_list')
    response = client.get(url, HTTP_AUTHORIZATION=f'Token {token.key}')
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert any(u['full_name'] == user.speaker_name for u in data)


@pytest.mark.django_db
def test_user_list_with_role_filter(client, django_user_model):
    group = Group.objects.create(name='Reviewer')
    user = django_user_model.objects.create(
        email="reviewer@example.com",
        speaker_name="Reviewer Name",
        bio="Some bio",
        verified=True,
        is_active=True,
    )
    user.groups.add(group)

    from core.models import Token
    token, _ = Token.objects.get_or_create(user=user)

    url = reverse('user_list')
    response = client.get(url, {'role': 'Reviewer'}, HTTP_AUTHORIZATION=f'Token {token.key}')
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert all(u['full_name'] == user.speaker_name for u in data)


@pytest.mark.django_db
def test_user_list_with_invalid_role_returns_404(client, django_user_model):
    user = django_user_model.objects.create(
        email="someuser@example.com",
        speaker_name="Some User",
        bio="Bio text",
        verified=True,
        is_active=True,
    )
    from core.models import Token
    token, _ = Token.objects.get_or_create(user=user)

    url = reverse('user_list')
    response = client.get(url, {'role': 'NotARealRole'}, HTTP_AUTHORIZATION=f'Token {token.key}')
    assert response.status_code == 404
