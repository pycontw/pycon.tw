import pytest

from events.models import Schedule


@pytest.fixture
def schedule(db):
    return Schedule.objects.create(html='mmm')
