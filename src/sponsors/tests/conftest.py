import pytest
from sponsors.models import Sponsor, OpenRole


@pytest.fixture
def create_sponsor_model(db):
    sponsor = Sponsor.objects.create(name="Test_Sponsor", intro="Test_intro", level=1)
    return sponsor


@pytest.fixture
def create_open_role_model(create_sponsor_model):
    openRole = OpenRole.objects.create(
        sponsor=create_sponsor_model,
        name="Test_open_role",
        description="Test_description",
    )
    return openRole
