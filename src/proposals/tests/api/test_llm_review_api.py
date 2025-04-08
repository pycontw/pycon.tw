import json

import pytest
from rest_framework.test import APIClient

from proposals.models import LLMReview


@pytest.fixture
def llm_review(talk_proposal):
    """Create a test LLM review fixture."""
    return LLMReview.objects.create(
        proposal=talk_proposal,
        summary="Test summary",
        comment="Test comment",
        translated_summary="Translated summary",
        translated_comment="Translated comment",
        vote="+1",
    )


def test_list_llm_reviews(api_client, llm_review):
    """Test listing all LLM reviews."""
    # Unauthenticated request should fail
    response = APIClient().get("/api/proposals/llm-reviews/")
    assert response.status_code == 401

    # Authenticated request should succeed
    response = api_client.get("/api/proposals/llm-reviews/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["summary"] == "Test summary"
    assert response.data[0]["vote"] == "+1"


def test_create_llm_review(api_client, talk_proposal):
    """Test creating a new LLM review."""
    data = {
        "proposal_id": talk_proposal.id,
        "summary": "New summary",
        "comment": "New comment",
        "translated_summary": "New translated summary",
        "translated_comment": "New translated comment",
        "vote": "+0",
    }

    # Unauthenticated request should fail
    response = APIClient().post(
        "/api/proposals/llm-reviews/",
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 401

    # Authenticated request should succeed
    response = api_client.post(
        "/api/proposals/llm-reviews/",
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 201

    # Verify the review was created
    created_review = LLMReview.objects.get(proposal=talk_proposal)
    assert created_review.summary == "New summary"
    assert created_review.vote == "+0"


def test_retrieve_llm_review(api_client, llm_review):
    """Test retrieving a specific LLM review."""
    # Unauthenticated request should fail
    response = APIClient().get(f"/api/proposals/llm-reviews/{llm_review.id}/")
    assert response.status_code == 401

    # Authenticated request should succeed
    response = api_client.get(f"/api/proposals/llm-reviews/{llm_review.id}/")
    assert response.status_code == 200
    assert response.data["summary"] == "Test summary"
    assert response.data["vote"] == "+1"


def test_update_llm_review(api_client, llm_review):
    """Test updating an existing LLM review."""
    data = {
        "proposal_id": llm_review.proposal.id,
        "summary": "Updated summary",
        "comment": "Updated comment",
        "translated_summary": "Updated translated summary",
        "translated_comment": "Updated translated comment",
        "vote": "-0",
    }

    # Unauthenticated request should fail
    response = APIClient().put(
        f"/api/proposals/llm-reviews/{llm_review.id}/",
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 401

    # Authenticated request should succeed
    response = api_client.put(
        f"/api/proposals/llm-reviews/{llm_review.id}/",
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 200

    # Verify the review was updated
    updated_review = LLMReview.objects.get(id=llm_review.id)
    assert updated_review.summary == "Updated summary"
    assert updated_review.vote == "-0"


def test_delete_llm_review(api_client, llm_review):
    """Test deleting an LLM review."""
    # Unauthenticated request should fail
    response = APIClient().delete(f"/api/proposals/llm-reviews/{llm_review.id}/")
    assert response.status_code == 401

    # Authenticated request should succeed
    response = api_client.delete(f"/api/proposals/llm-reviews/{llm_review.id}/")
    assert response.status_code == 204

    # Verify the review was deleted
    assert not LLMReview.objects.filter(id=llm_review.id).exists()


def test_get_llm_review_by_proposal(api_client, llm_review):
    """Test retrieving an LLM review by proposal ID."""
    proposal_id = llm_review.proposal.id

    # Unauthenticated request should fail
    response = APIClient().get(f"/api/proposals/llm-reviews/proposal/{proposal_id}/")
    assert response.status_code == 401

    # Authenticated request should succeed
    response = api_client.get(f"/api/proposals/llm-reviews/proposal/{proposal_id}/")
    assert response.status_code == 200
    assert response.data["summary"] == "Test summary"
    assert response.data["vote"] == "+1"

    # Test with non-existent proposal ID
    non_existent_id = 9999
    response = api_client.get(f"/api/proposals/llm-reviews/proposal/{non_existent_id}/")
    assert response.status_code == 404
