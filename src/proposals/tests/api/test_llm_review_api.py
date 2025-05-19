import json

import pytest
from rest_framework.test import APIClient

from proposals.models import LLMReview


@pytest.fixture
def llm_review(talk_proposal):
    """Create a test LLM review fixture."""
    return LLMReview.objects.create(
        proposal=talk_proposal,
        stage=LLMReview.STAGE_1,
        categories=["PRAC"],
        summary="Test summary",
        comment="Test comment",
        translated_summary="Translated summary",
        translated_comment="Translated comment",
        vote="+1",
        stage_diff="",
        translated_stage_diff="",
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
    assert response.data[0]["stage"] == LLMReview.STAGE_1
    assert response.data[0]["categories"] == ["PRAC"]


def test_create_llm_review(api_client, talk_proposal):
    """Test creating a new LLM review."""
    data = {
        "proposal_id": talk_proposal.id,
        "stage": LLMReview.STAGE_1,
        "categories": ["PRAC", "CORE"],
        "summary": "New summary",
        "comment": "New comment",
        "translated_summary": "New translated summary",
        "translated_comment": "New translated comment",
        "vote": "+0",
        "stage_diff": "Diff text",
        "translated_stage_diff": "Translated diff text",
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
    # Query for the specific stage to ensure uniqueness if multiple stages are tested elsewhere
    created_review = LLMReview.objects.get(proposal=talk_proposal, stage=LLMReview.STAGE_1)
    assert created_review.summary == "New summary"
    assert created_review.vote == "+0"
    assert created_review.categories == ["PRAC", "CORE"]
    assert created_review.stage == LLMReview.STAGE_1
    assert created_review.stage_diff == "Diff text"


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
    assert response.data["stage"] == LLMReview.STAGE_1
    assert response.data["categories"] == ["PRAC"]


def test_update_llm_review(api_client, llm_review):
    """Test updating an existing LLM review."""
    data = {
        "proposal_id": llm_review.proposal.id,
        "stage": LLMReview.STAGE_1,
        "categories": ["CORE"],
        "summary": "Updated summary",
        "comment": "Updated comment",
        "translated_summary": "Updated translated summary",
        "translated_comment": "Updated translated comment",
        "vote": "-0",
        "stage_diff": "Updated diff",
        "translated_stage_diff": "Updated translated diff",
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
    assert updated_review.categories == ["CORE"]
    assert updated_review.stage == LLMReview.STAGE_1
    assert updated_review.stage_diff == "Updated diff"


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
    # This test assumes the endpoint returns a single review (e.g., stage 1 or the first one)
    # If it returns a list, assertions need to change (e.g., response.data[0][\"summary\"])
    response = api_client.get(f"/api/proposals/llm-reviews/proposal/{proposal_id}/")
    assert response.status_code == 200
    # If API returns a list of reviews for the proposal:
    if isinstance(response.data, list):
        assert len(response.data) > 0
        review_data = response.data[0] # Check the first review
        assert review_data["summary"] == "Test summary"
        assert review_data["vote"] == "+1"
        assert review_data["stage"] == LLMReview.STAGE_1
        assert review_data["categories"] == ["PRAC"]
    else: # Assuming it returns a single object as before
        assert response.data["summary"] == "Test summary"
        assert response.data["vote"] == "+1"
        assert response.data["stage"] == LLMReview.STAGE_1
        assert response.data["categories"] == ["PRAC"]

    # Test with non-existent proposal ID
    non_existent_id = 9999
    response = api_client.get(f"/api/proposals/llm-reviews/proposal/{non_existent_id}/")
    assert response.status_code == 404
