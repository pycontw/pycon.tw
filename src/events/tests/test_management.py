import io
import json
import unittest.mock

import pytest

from django.core.management import call_command

from events.models import KeynoteEvent


@pytest.fixture
def keynote_event_json():
    return json.dumps({
        "events.KeynoteEvent": [
            {
                "slug": "audrey-tang",
                "speaker_name": "Audrey Tang",
                "time": [1, "9:30", "10:30"],
                "location": "ALL"
            }
        ]
    })


class MockFile(unittest.mock.MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(spec=io.FileIO, *args, **kwargs)


class MockOpen(unittest.mock.Mock):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mock_file = MockFile()
        mock_file.configure_mock(**{'__enter__.return_value': mock_file})
        self.return_value = mock_file

    def mock_set_readout(self, value):
        self.configure_mock(**{'return_value.read.return_value': value})


@pytest.fixture
def mock_open(mocker):
    mock_open = mocker.patch(
        'events.management.commands.import_events.open',
        create=True, new_callable=MockOpen,
    )
    return mock_open


@pytest.mark.django_db
def test_import_keynote_event(djutils, mock_open, keynote_event_json):
    mock_open.mock_set_readout(keynote_event_json)

    KeynoteEvent.objects.create(speaker_name='Amber Brown', slug='amber-brown')
    call_command('import_events', 'yks.om')

    mock_open.assert_called_once_with('yks.om')
    assert djutils.to_list(KeynoteEvent.objects.order_by('pk')) == [
        '<KeynoteEvent: Keynote: Amber Brown>',
        '<KeynoteEvent: Keynote: Audrey Tang>',
    ]


@pytest.mark.django_db
def test_import_keynote_event_truncate(djutils, mock_open, keynote_event_json):
    mock_open.mock_set_readout(keynote_event_json)

    KeynoteEvent.objects.create(speaker_name='Amber Brown', slug='amber-brown')
    call_command('import_events', 'yks.om', truncate=True)

    mock_open.assert_called_once_with('yks.om')
    assert djutils.to_list(KeynoteEvent.objects.all()) == [
        '<KeynoteEvent: Keynote: Audrey Tang>',
    ]
