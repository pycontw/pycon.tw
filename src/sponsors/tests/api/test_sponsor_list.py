from sponsors.models import Sponsor

endpoint = "/api/sponsors/"


def test_sponsor_list(user, drf_api_client, create_sponsor_model):
    response = drf_api_client.get(endpoint)
    assert response.status_code == 401
    drf_api_client.force_authenticate(user=user)
    response = drf_api_client.get(endpoint)

    data = response.json()["data"]

    targetSponsor = Sponsor.objects.get(id=create_sponsor_model.id)

    assert len(data) == Sponsor.objects.count()
    assert len(data[0]["sponsors"]) == 1

    assert data[0]["level_name"] == targetSponsor.level_en_name
    assert data[0]["sponsors"][0]["name_en_us"] == targetSponsor.name_en_us
    assert response.status_code == 200
