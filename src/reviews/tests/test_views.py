from unittest.mock import patch

import pytest
from django.urls import reverse


@pytest.fixture
def review_stages_url():
    return reverse('review_stages')

@pytest.mark.django_db
def test_review_stages_get(client, review_stages_url):
    response = client.get(review_stages_url)

    assert response.status_code == 200
    assert 'review_stages_list' in response.context
    assert 'current_review_stages_setting' in response.context

@pytest.mark.django_db
@patch('reviews.views.reg')
@patch('reviews.views.messages')
def test_review_stages_post_valid_data(mock_messages, mock_reg, client, review_stages_url):
    mock_reg.get.return_value = ''
    mock_reg.__setitem__.side_effect = lambda key, value: None

    post_data = {
        'proposals.creatable': 'True',
        'proposals.editable': 'True',
        'proposals.withdrawable': 'True',
        'reviews.visible.to.submitters': 'True',
        'reviews.stage': '1',
        'proposals.disable.after': '2024-12-31T12:00',
        'review_timezone': 'UTC',
    }

    response = client.post(review_stages_url, post_data)

    assert response.status_code == 200
    mock_messages.info.assert_called_once_with(
        response.wsgi_request, 'This setting has been changed successfully.'
    )

@pytest.mark.django_db
@patch('reviews.views.reg')
@patch('reviews.views.messages')
def test_review_stages_post_invalid_date(mock_messages, mock_reg, client, review_stages_url):
    post_data = {
        'proposals.creatable': 'True',
        'proposals.editable': 'True',
        'proposals.withdrawable': 'True',
        'reviews.visible.to.submitters': 'True',
        'reviews.stage': '1',
        'proposals.disable.after': 'invalid-date',
        'review_timezone': '',
    }

    response = client.post(review_stages_url, post_data)

    assert response.status_code == 200
    mock_messages.error.assert_called_once_with(
        response.wsgi_request, 'Please input valid date format : " + "%Y-%m-%dT%H:%M'
    )

@pytest.mark.django_db
def test_review_stages_timezone_conversion(client, review_stages_url):
    post_data = {
        'proposals.creatable': 'True',
        'proposals.editable': 'True',
        'proposals.withdrawable': 'True',
        'reviews.visible.to.submitters': 'True',
        'reviews.stage': '1',
        'proposals.disable.after': '2024-12-31T12:00',
        'review_timezone': 'Asia/Taipei',
    }

    with patch('reviews.views.pytz.timezone') as mock_timezone:
        mock_timezone.return_value.localize.return_value.strftime.return_value = '2024-12-31 12:00:00-0500'
        response = client.post(review_stages_url, post_data)

    assert response.status_code == 200
    assert mock_timezone.call_count == 1
    assert mock_timezone.called_with('Asia/Taipei')
