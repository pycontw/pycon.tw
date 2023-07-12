import pytest
from django.conf import settings
from registry.helper import reg
from attendee.models import Attendee
from core.models import Token


@pytest.mark.parametrize('attendee_token,status,num_channel', [
    ('123', 400, 0),
    ('1234', 200, 0),
    ('1234', 200, 1),
    ('1234', 200, 2),
])
@pytest.mark.django_db
def test_attendee(drf_api_client, bare_user, attendee_token, status, num_channel):
    token = Token.objects.get_or_create(user=bare_user)
    drf_api_client.credentials(HTTP_AUTHORIZATION="Token " + str(token[0]))
    attendee = Attendee(token="1234")
    attendee.save()  # insert to database
    # add slug
    key_prefix = f"{settings.CONFERENCE_DEFAULT_SLUG}.live."
    reg["pycontw-1999.live.r1"] = "video_old_id"  # unrelated
    for i in range(num_channel):
        reg[f"{key_prefix}r{i}"] = f"video_id_{i}"

    # test
    response = drf_api_client.post('/api/attendee/verify/', data={"token": attendee_token})
    assert response.status_code == status
    if status == 200:
        assert len(response.json()["youtube_infos"]) == num_channel
