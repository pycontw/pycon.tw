import pytest
from django.conf import settings

endpoint = "/ccip"

@pytest.mark.django_db
def test_ccip_api_view(client, sample_tags):

    response = client.get(endpoint, follow=True)
    assert response.status_code == 200

    data = response.json()

    assert 'tags' in data
    assert isinstance(data['tags'], list)
    print("data:", data)
    assert data['tags'][0]['en']['name'] == "English talk"
