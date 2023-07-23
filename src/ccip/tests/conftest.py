import pytest
from unittest.mock import Mock
from events.models import (
    CustomEvent, KeynoteEvent,
    ProposedTalkEvent, ProposedTutorialEvent,
    SponsoredEvent,
)

@pytest.fixture
def sample_tags():
    tags = [
        {
            "id": "lng-ENEN",
            "zh": {},
            "en": {
                "name": "English talk"
            }
        },
    ]
    return tags