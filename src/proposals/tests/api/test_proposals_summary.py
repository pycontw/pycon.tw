endpoint = "/api/proposals/summary/"


def test_proposals_summary(
    user,
    drf_api_client,
    talk_proposal,
    tutorial_proposal,
    stage_1_review,
    stage_2_review,
):
    response = drf_api_client.get(endpoint)
    assert response.status_code == 401

    drf_api_client.force_authenticate(user=user)
    response = drf_api_client.get(endpoint)
    data = response.data

    assert data["num_proposed_talk"] == 1
    assert data["num_proposed_tutorial"] == 1
    assert data["num_stage_1_reviews"] == 2
    assert data["num_stage_2_reviews"] == 1
    assert response.status_code == 200
