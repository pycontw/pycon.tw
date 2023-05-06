from sponsors.models import OpenRole

endpoint = "/api/sponsors/jobs/"


def test_jobs_list(user, drf_api_client, create_open_role_model):
    response = drf_api_client.get(endpoint)
    assert response.status_code == 401

    drf_api_client.force_authenticate(user=user)
    response = drf_api_client.get(endpoint)
    data = response.json()["data"]
    targetOpenRole = OpenRole.objects.get(sponsor=create_open_role_model.sponsor)

    assert len(data) == OpenRole.objects.count()
    assert data[0]["sponsor_name"] == create_open_role_model.sponsor.name

    assert data[0]["jobs"][0]["job_name_en_us"] == targetOpenRole.name_en_us

    assert response.status_code == 200
